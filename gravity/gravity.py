import pygame
from pygame import gfxdraw
import numpy as np
from numba import njit
import sys

# Globals
FRAMERATE = 60
WHITE = (255, 255, 255)
BLUE = (105, 151, 188)
GREEN = (100, 177, 92)
RED = (254, 131, 35)
BLACK = (24, 27, 40)
screenSize = (1280, 768)
screenCenter = [i // 2 for i in screenSize]
planetDefaultMass = 50
planetDefaultColour = GREEN
planetDefaultSize = 5
sunDefaultMass = 3000
sunDefaultColour = RED
sunDefaultSize = 10
sunFixed = True
pathPredictionColour = BLUE
pathPredictionLength = 1000
pathPredictionSize = 2
pathPredictionInterval = 5
mouseVelocityFactor = 0.04
minimumDistance = 20


def getMousePos():
    pos = pygame.mouse.get_pos()
    return pos


def drawCircle(pos=None, colour=planetDefaultColour, size=planetDefaultSize):
    if pos is None:
        pos = getMousePos()
    pos = [min(max(screenSize) + 20, max(-20, int(x))) for x in pos]
    gfxdraw.aacircle(screen, *pos, size, colour)


def spawnBody(
    r=screenCenter, m=planetDefaultMass, v=(0, 0), colour=planetDefaultColour, size=planetDefaultSize, is_sun=False,
):
    global bodys_m_and_r
    bodys.append(Body(r=r, m=m, v=v, colour=colour, size=size, is_sun=is_sun))
    bodys_m_and_r = np.append(bodys_m_and_r, [[m, r[0], r[1]]], axis=0)


def reset():
    global bodys, bodys_m_and_r
    bodys = []
    bodys_m_and_r = np.empty((0, 3), dtype=np.float32)  # to speed up path prediction
    spawnBody(m=sunDefaultMass, colour=sunDefaultColour, size=sunDefaultSize, is_sun=sunFixed)


class Body:
    def __init__(self, r, m, v, colour, size, is_sun):
        self.m = m
        self.r = np.array(r, dtype=np.float32)
        self.v = mouseVelocityFactor * np.array(v, dtype=np.float32)
        self.a = np.array([0, 0], dtype=np.float32)
        self.colour = np.array(colour, dtype=np.int32)
        self.size = size
        self.is_sun = is_sun

    def update(self, body_number):
        if not self.is_sun:
            self._update(self.r, self.v, self.a, bodys_m_and_r, body_number)

    @staticmethod
    @njit
    def _update(r, v, a, m_r_array, body_number):
        a[:] = 0
        for i in range(m_r_array.shape[0]):
            body_m = m_r_array[i, 0]
            body_r = m_r_array[i, 1:]
            delta_r = body_r - r
            a += body_m / max(minimumDistance, delta_r.dot(delta_r)) ** (1.5) * delta_r

        v += a
        r += v
        m_r_array[body_number, 1:] = r

    def draw(self):
        drawCircle(pos=self.r, colour=self.colour, size=self.size)


class PathPrediction:
    def __init__(self):
        self.active = 0
        self.start = np.array([0, 0], dtype=np.float32)
        self.r = np.array([0, 0], dtype=np.float32)
        self.v = np.array([0, 0], dtype=np.float32)
        self.a = np.array([0, 0], dtype=np.float32)
        self.path = np.zeros((pathPredictionLength, 2), dtype=np.int32)

    def update(self):
        if pygame.mouse.get_pressed()[0] == 1:
            mouse_cur_pos = pygame.mouse.get_pos()
            self.r[:] = self.start
            self.v = mouseVelocityFactor * (self.start - mouse_cur_pos)

            # where the magic happens
            self._iterate(self.r, self.v, self.a, bodys_m_and_r, self.path)

    @staticmethod
    @njit
    def _iterate(r, v, a, m_r_array, path_array):
        for i in range(pathPredictionLength):
            a[:] = 0
            body_m = m_r_array[0, 0]
            body_r = m_r_array[0, 1:]
            delta_r = body_r - r
            a += body_m / max(minimumDistance, delta_r.dot(delta_r)) ** (1.5) * delta_r

            v += a
            r += v
            path_array[i, :] = r

    def draw(self):
        if self.active:
            for i in range(0, self.path.shape[0], pathPredictionInterval):
                drawCircle(
                    pos=self.path[i, :], colour=pathPredictionColour, size=pathPredictionSize,
                )


def main():
    global screen, bodys, bodys_m_and_r
    running = True

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("gravity.py")
    bodys = []
    bodys_m_and_r = np.empty((0, 3), dtype=np.float32)  # to speed up path prediction
    spawnBody(m=sunDefaultMass, colour=sunDefaultColour, size=sunDefaultSize, is_sun=sunFixed)
    predictor = PathPrediction()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down_pos = pygame.mouse.get_pos()
                predictor.active = 1
                predictor.start[:] = mouse_down_pos

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up_pos = pygame.mouse.get_pos()
                spawnBody(
                    r=mouse_down_pos, v=[b - a for a, b in zip(mouse_up_pos, mouse_down_pos)],
                )
                predictor.active = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    reset()

            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for i, body in enumerate(bodys):
            body.draw()
            body.update(i)

        predictor.update()
        predictor.draw()

        pygame.display.update()
        clock.tick(FRAMERATE)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
