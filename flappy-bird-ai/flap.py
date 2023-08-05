import pygame
import sys
import random

# init pygame
pygame.init()
pygame.display.set_caption("FlapPy Bird")
W, H = (int(0.5 * i) for i in (576, 1024))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
font = pygame.font.Font("assets/04B_19.ttf", 30)

# init game variables
game_active = True
framerate = 144
g = 0.125


class Bird:
    start_x = 50
    start_y = H // 3
    max_dy = 6
    jump_impulse = 4

    def __init__(self):
        self.colour = random.choice(["blue", "red", "yellow"])
        self.surface = pygame.image.load(
            f"assets/{self.colour}bird-upflap.png"
        ).convert_alpha()
        self.rect = self.surface.get_rect(
            center=(type(self).start_x, type(self).start_y)
        )
        self.dy = 0

    def check_collisions(self, pipes):
        if self.rect.top <= -100 or self.rect.bottom >= H - 112:
            Sounds.play("die")
            return False
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect) or self.rect.colliderect(pipe.rect_inv):
                Sounds.play("die")
                return False
        return True

    def update(self):
        self.rect.centery += self.dy
        self.dy += g
        self.dy = min(type(self).max_dy, self.dy)

    def draw(self):
        rotated = pygame.transform.rotozoom(self.surface, -self.dy * 3, 1)
        screen.blit(rotated, self.rect)


class Pipe:
    spacing_y = 150
    despawn_x = -30
    colour = random.choice(["green", "red"])
    surface = pygame.image.load(f"assets/pipe-{colour}.png")
    surface_inv = pygame.transform.flip(surface, False, True)

    def __init__(self):
        self.y = random.randint(int(0.2 * H), int(0.6 * H))
        self.rect = type(self).surface.get_rect(
            midtop=(W + 30, self.y + type(self).spacing_y // 2)
        )
        self.rect_inv = type(self).surface_inv.get_rect(
            midbottom=(W + 30, self.y - type(self).spacing_y // 2)
        )

    def draw(self):
        screen.blit(type(self).surface, self.rect)
        screen.blit(type(self).surface_inv, self.rect_inv)

    def update(self):
        self.rect.centerx -= 1
        self.rect_inv.centerx -= 1


class Sounds:
    sounds = dict(
        flap=pygame.mixer.Sound("sound/sfx_wing.wav"),
        die=pygame.mixer.Sound("sound/sfx_hit.wav"),
        point=pygame.mixer.Sound("sound/sfx_point.wav"),
        swoosh=pygame.mixer.Sound("sound/sfx_swooshing.wav"),
    )
    play_sounds = True

    @classmethod
    def play(cls, sound):
        if cls.play_sounds:
            cls.sounds[sound].play()


class Score:
    score = 0
    high_score = 0
    score_timeout = False

    @classmethod
    def update(cls, pipes):
        for pipe in pipes:
            if (
                Bird.start_x - 5 < pipe.rect.centerx
                and pipe.rect.centerx < Bird.start_x + 5
            ):
                if not cls.score_timeout:
                    cls.score += 1
                    Sounds.play("point")
                cls.score_timeout = True
                return
        cls.score_timeout = False

        cls.high_score = max(int(cls.score), cls.high_score)

    @classmethod
    def draw(cls, game_active, x=W // 2, y=50):
        if game_active:
            score_surface = font.render(f"{int(cls.score)}", False, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(x, y))
            screen.blit(score_surface, score_rect)

        else:
            score_surface = font.render(
                f"Score: {int(cls.score)}", False, (255, 255, 255)
            )
            score_rect = score_surface.get_rect(center=(x, y))
            screen.blit(score_surface, score_rect)

            score_surface = font.render(
                f"High score: {int(cls.high_score)}", False, (0, 0, 0)
            )
            score_rect = score_surface.get_rect(center=(W // 2, H - 50))
            screen.blit(score_surface, score_rect)

    @classmethod
    def reset(cls):
        cls.score = 0
        cls.score_timeout = False


class Floor:
    surface = pygame.image.load("assets/base.png").convert()

    def __init__(self):
        self.x = 0

    def draw(self):
        screen.blit(type(self).surface, (self.x, H - 112))
        screen.blit(type(self).surface, (self.x + W, H - 112))

    def update(self):
        self.x -= 1
        if self.x <= -W:
            self.x = 0


class Background:
    background = pygame.image.load(
        f"assets/background-{random.choice(['night', 'day'])}.png"
    ).convert()

    @classmethod
    def draw(cls):
        screen.blit(cls.background, (0, 0))


class GameOverScreen:
    game_over_surface = pygame.image.load("assets/gameover.png").convert_alpha()
    game_over_rect = game_over_surface.get_rect(center=(W // 2, H // 2))

    @classmethod
    def draw(cls):
        screen.blit(cls.game_over_surface, cls.game_over_rect)

def reset_and_delay():
    for _ in range(120):
        Background.draw()
        floor.draw()
        bird.draw()
        pygame.display.update()
        clock.tick(framerate)

if __name__ == "__main__":
    # init pipes logic
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, framerate * 10)

    pipes = [Pipe()]
    floor = Floor()
    bird = Bird()

    reset_and_delay()
    
    # GAME LOOP
    while True:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controls:
            # UP to flap wings
            # SPACE to restart game after dying
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    bird.dy = -Bird.jump_impulse
                    if game_active:
                        Sounds.play("flap")
                if event.key == pygame.K_SPACE and not game_active:
                    Sounds.play("swoosh")
                    game_active = True
                    pipes = []
                    bird.rect.centery = Bird.start_y
                    bird.dy = 0
                    Score.reset()
                    reset_and_delay()
            if event.type == SPAWNPIPE:
                pipes.append(Pipe())

        Background.draw()

        # draw, animate pipes, then despawn old pipes
        for pipe in pipes:
            pipe.draw()
            if game_active:
                pipe.update()
        pipes = [pipe for pipe in pipes if pipe.rect.right > Pipe.despawn_x]

        floor.draw()
        bird.draw()
        Score.draw(game_active)

        if game_active:
            game_active = bird.check_collisions(pipes)

        if game_active:
            bird.update()
            floor.update()
            Score.update(pipes)
        else:
            GameOverScreen.draw()

        pygame.display.update()
        clock.tick(framerate)
