import random
import pygame

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
JUMPSIZE = GRAVITY * 10
BIRD_SIZE = 30
BIRD_COLOR = RED

# Pipes
PIPE_WIDTH = 75
PIPE_COLOR = GREEN
PIPE_MOVEMENT = 5
PIPE_HOLE_SIZE = BIRD_SIZE * 4
hole_count = 4
PIPE_HEIGHT_LIST = [WIN_HEIGHT // hole_count * i for i in range(2, hole_count)]


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
        self.hole = PIPE_HOLE_SIZE
        self.rect1 = pygame.Rect(self.x, WIN_HEIGHT - self.height, self.width, self.height)
        self.rect2 = pygame.Rect(self.x, 0, self.width, WIN_HEIGHT - self.height - self.hole)

    def update(self):
        self.x -= self.movement
        self.rect1 = pygame.Rect(self.x, WIN_HEIGHT - self.height, self.width, self.height)
        self.rect2 = pygame.Rect(self.x, 0, self.width, WIN_HEIGHT - self.height - self.hole)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect1)
        pygame.draw.rect(screen, self.color, self.rect2)


class FlappyBird:
    def __init__(self):
        self.bird = Bird()
        self.pipes = Pipe(WIN_WIDTH, random.choice(PIPE_HEIGHT_LIST))

        self.winSize = (WIN_WIDTH, WIN_HEIGHT)
        self.screen = pygame.display.set_mode(self.winSize)
        pygame.display.init()
        pygame.display.set_caption("myFlappyBird")
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.running = True
        self.BLACK = BLACK

        self.score = 0

    def update(self):
        self.bird.update()
        self.bird.draw(screen=self.screen)

        self.pipes.update()
        self.pipes.draw(screen=self.screen)

        if self.pipes.x < -self.pipes.width:
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

            collision = self.check_collision()
            if collision:
                self.running = False

            pygame.display.flip()
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

        pygame.quit()


if __name__ == "__main__":
    fb = FlappyBird()
    fb.run()
