"""
Minimalistic implementation of DDPM following https://github.com/cloneofsimo/minDiffusion,
for learning purposes
"""

import torch
from torch import nn
import numpy as np
from torchvision import datasets, transforms
from torchvision.utils import save_image, make_grid
from tqdm import tqdm
import argparse
import os
import datetime


class Network(nn.Module):
    def __init__(self, nchannels) -> None:
        super().__init__()

        self.nfeatures = [
            (nchannels, 64),
            (64, 128),
            (128, 256),
            (256, 512),
            (512, 256),
            (256, 128),
            (128, 64),
            (64, nchannels),
        ]

        self.conv = nn.Sequential(
            *[
                nn.Sequential(
                    nn.Conv2d(ic, oc, 7, padding=3),
                    nn.BatchNorm2d(oc),
                    nn.LeakyReLU(),
                )
                for ic, oc in self.nfeatures[:-1]
            ],
            nn.Conv2d(*self.nfeatures[-1], 3, padding=1),
        )

    def forward(self, x, t):
        return self.conv(x)


class DDPM(nn.Module):
    def __init__(self, args) -> None:
        super().__init__()

        self.imgdim = args.imgdim
        self.nchannels = args.nchannels
        self.nsteps = args.nsteps
        self.device = args.device

        self.betas = torch.linspace(1e-4, 0.02, steps=self.nsteps + 1,).to(
            args.device
        )[..., None, None, None]
        self.alphas = 1 - self.betas
        self.alphas_b = torch.cumprod(self.alphas, dim=0)
        self.sqrt_alphas_b = torch.sqrt(self.alphas_b)
        self.sqrt_one_minus_alphas_b = torch.sqrt(1 - self.alphas_b)
        self.one_over_sqrt_alphas = 1 / torch.sqrt(self.alphas)
        self.eps_coef = (1 - self.alphas) / (self.sqrt_one_minus_alphas_b)
        self.sigmas = torch.sqrt(self.betas)

        self.network = Network(self.nchannels)

    def forward(self, x0, eps, t):
        return self.network(
            self.sqrt_alphas_b[t] * x0 + self.sqrt_one_minus_alphas_b[t] * eps,
            t,
        )

    def sample(self, n):
        x = torch.randn(size=(n, self.nchannels, self.imgdim, self.imgdim)).to(
            self.device
        )

        with torch.no_grad():
            for t in range(self.nsteps, 0, -1):
                z = torch.randn_like(x)
                x = self.reverse_step(x, z, t)

            return self.reverse_step(x, 0, 0)

    def reverse_step(self, x, z, t):
        return (
            self.one_over_sqrt_alphas[t] * (x - self.eps_coef[t] * self.network(x, t))
            + self.sigmas[t] * z
        )


def eval(diffusion_model, args, epoch=0):
    sample = diffusion_model.sample(n=4)
    grid = make_grid(sample, nrow=2)
    save_image(grid, args.save_dir + f"/epoch_{epoch}.png")


def train(diffusion_model, loader, args):
    opt = torch.optim.AdamW(diffusion_model.parameters(), lr=args.lr)
    loss_fn = torch.nn.MSELoss()

    for epoch in range(args.nepochs):
        print("-" * 40 + f"\nEPOCH: {epoch}\n" + "-" * 40)

        diffusion_model.train()
        pbar = tqdm(loader)
        loss_ema = None
        for i, (x, _) in enumerate(pbar):
            opt.zero_grad()
            x = x.to(args.device)

            t = torch.randint(1, args.nsteps, size=(x.shape[0],))
            eps = torch.randn_like(x)
            eps_pred = diffusion_model(x, eps, t)

            loss = loss_fn(eps, eps_pred)
            loss.backward()

            opt.step()

            if not loss_ema:
                loss_ema = loss.item()
            else:
                loss_ema = 0.9 * loss_ema + 0.1 * loss.item()
            pbar.set_description(f"Loss: {loss_ema:.4f}")

        diffusion_model.eval()
        eval(diffusion_model, args, epoch)

        torch.save(diffusion_model.state_dict(), args.save_dir + f"/epoch_{epoch}.pt")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--lr", type=float, help="learning rate", default=2e-4)
    parser.add_argument(
        "--nsteps", type=int, help="number of diffusion steps per sample", default=100
    )
    parser.add_argument("--nepochs", type=int, help="number of epochs", default=25)
    parser.add_argument("--nchannels", type=int, help="number of channels", default=1)
    parser.add_argument("--imgdim", type=int, help="dimension of images", default=28)
    parser.add_argument("--batch_size", type=int, help="batch_size", default=128)
    parser.add_argument("--save_dir", help="directory to save in", default="")
    parser.add_argument("--device", help="GPU/CPU", default="cuda")
    args = parser.parse_args()

    if not args.save_dir:
        args.save_dir = (
            f"./results/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        )
    os.makedirs(args.save_dir, exist_ok=True)

    dataset = datasets.MNIST(
        "./data",
        train=True,
        download=True,
        transform=transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.0,), (1.0,)),
            ]
        ),
    )

    loader = torch.utils.data.DataLoader(
        dataset, batch_size=args.batch_size, shuffle=True, num_workers=4
    )

    diffusion_model = DDPM(args).to(args.device)
    diffusion_model = torch.compile(diffusion_model)

    train(diffusion_model, loader, args)
