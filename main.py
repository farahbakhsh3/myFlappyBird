import random
import pygame
import time

# PyGame
WIN_WIDTH = 600
WIN_HEIGHT = 800
FPS = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Bird
GRAVITY = 2
GRAVITY_INCREASE_RATE = 1.05
JUMPSIZE = GRAVITY * 8
BIRD_SIZE = 30
BIRD_COLOR = YELLOW

# Pipes
PIPE_WIDTH = 65
PIPE_COLOR = GREEN
PIPE_MOVEMENT = 7
PIPE_HOLE_SIZE = BIRD_SIZE * 3
PIPE_HEIGHT_LIST = [200, 300, 400, 500, 600, 700]


class Bird:
    def __init__(self):
        self.y = WIN_HEIGHT // 2
        self.x = WIN_HEIGHT // 4
        self.gravity = GRAVITY
        self.jumpSize = JUMPSIZE
        self.size = BIRD_SIZE
        self.color = BIRD_COLOR
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y += self.gravity
        self.gravity *= GRAVITY_INCREASE_RATE
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def jump(self):
        self.y -= self.jumpSize
        self.gravity = GRAVITY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.width = PIPE_WIDTH
        self.movement = PIPE_MOVEMENT
        self.color = PIPE_COLOR
        self.hole_size = PIPE_HOLE_SIZE
        self.rect1 = pygame.Rect(self.x, WIN_HEIGHT - self.height, self.width, self.height)
        self.rect2 = pygame.Rect(self.x, 0, self.width, WIN_HEIGHT - self.height - self.hole_size)

    def update(self):
        self.x -= self.movement
        self.rect1 = pygame.Rect(self.x, WIN_HEIGHT - self.height, self.width, self.height)
        self.rect2 = pygame.Rect(self.x, 0, self.width, WIN_HEIGHT - self.height - self.hole_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect1)
        pygame.draw.rect(screen, self.color, self.rect2)


class FlappyBird:
    def __init__(self):
        self.winSize = (WIN_WIDTH, WIN_HEIGHT)
        self.screen = pygame.display.set_mode(self.winSize)
        pygame.display.init()
        pygame.display.set_caption("myFlappyBird")
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.running = True
        self.BLACK = BLACK

        self.restart()

    def update(self):
        self.bird.update()
        self.bird.draw(screen=self.screen)

        self.pipes.update()
        self.pipes.draw(screen=self.screen)

        if self.pipes.x < -self.pipes.width:
            self.pipes = Pipe(WIN_WIDTH, random.choice(PIPE_HEIGHT_LIST))
            self.score += 1
            print(self.score)

    def restart(self):
        self.running = True
        self.score = 0

        self.bird = Bird()
        self.pipes = Pipe(WIN_WIDTH, random.choice(PIPE_HEIGHT_LIST))

    def check_collision(self):
        if (self.bird.y + self.bird.size > WIN_HEIGHT
                or self.bird.y < 0):
            return True

        collide = (pygame.Rect.colliderect(self.bird.rect, self.pipes.rect1) or
                   (pygame.Rect.colliderect(self.bird.rect, self.pipes.rect2)))
        return collide

    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.bird.jump()
            elif keys[pygame.K_ESCAPE]:
                self.running = False

            self.screen.fill(self.BLACK)
            self.update()

            pygame.display.update()
            self.clock.tick(self.fps)

            collision = self.check_collision()
            if collision:
                self.restart()
                pygame.draw.rect(self.screen, RED,
                                 (WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 - 100, 300, 200))
                pygame.display.update()
                time.sleep(1.5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

        pygame.quit()


if __name__ == "__main__":
    fb = FlappyBird()
    fb.run()
