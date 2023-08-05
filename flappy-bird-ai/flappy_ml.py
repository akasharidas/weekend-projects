import neat
import pickle
import pygame
import sys

# This line inits pygame too
from flap import Bird, Floor, Pipe, Score, Background, Sounds, clock, screen, font

Sounds.play_sounds = False
gen_number = 0
cont_score_increment = 0.02


def draw_gen_number(gen_number, x=50, y=25):
    surface = font.render(f"Gen: {int(gen_number)}", False, (255, 255, 255))
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def get_pipe_params(pipes, bird_x):
    for pipe in pipes:
        if pipe.rect.topright[0] + 10 >= bird_x:
            break

    return (
        pipe.rect.centerx,
        (pipe.rect.midtop[1] + pipe.rect_inv.midbottom[1]) / 2,
    )


def eval_genomes(genomes, config):
    global gen_number
    gen_number += 1

    # init game variables
    game_active = True
    framerate = 144
    cont_score = 0

    # init pipes logic
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, framerate * 10)

    pipes = [Pipe()]
    floor = Floor()
    birds = [(i, Bird()) for i in range(len(genomes))]
    nets = [
        (i, neat.nn.FeedForwardNetwork.create(genome, config)) for i, genome in genomes
    ]

    # GAME LOOP
    while True:
        cont_score += cont_score_increment

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SPAWNPIPE:
                pipes.append(Pipe())

        for bird_id, bird in birds:
            inputs = [
                bird.rect.centery,
                bird.dy,
                Bird.start_x,
                *get_pipe_params(pipes, Bird.start_x),
            ]
            output = nets[bird_id][1].activate(inputs)
            if output[0] > 0.5:
                bird.dy = -Bird.jump_impulse
            genomes[bird_id][1].fitness = Score.score + cont_score

        Background.draw()

        if not birds:
            Score.reset()
            break

        # draw, animate pipes, then despawn old pipes
        for pipe in pipes:
            pipe.draw()
            if game_active:
                pipe.update()
        pipes = [pipe for pipe in pipes if pipe.rect.right > Pipe.despawn_x]

        floor.draw()
        for bird in birds:
            bird[1].draw()
        Score.draw(game_active, x=260, y=25)
        draw_gen_number(gen_number)

        birds[:] = [bird for bird in birds if bird[1].check_collisions(pipes)]

        for bird in birds:
            bird[1].update()
        floor.update()
        Score.update(pipes)

        pygame.display.update()
        clock.tick(framerate)


def run(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(eval_genomes, 300)


if __name__ == "__main__":
    run("config.ini")
