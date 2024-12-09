import random
import pygame
import time

# PyGame
WIN_WIDTH = 600
WIN_HEIGHT = 800
FPS = 50
FPS_RATE = 0.01

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Bird
GRAVITY = 1.0
GRAVITY_INCREASE_RATE = 1.05
JUMPSIZE = GRAVITY + 5
BIRD_SIZE = 30
BIRD_COLOR = YELLOW

# Pipes
PIPE_WIDTH = 75
PIPE_COLOR = GREEN
PIPE_MOVEMENT = 4
PIPE_HOLE_SIZE = BIRD_SIZE * 3
PIPE_HEIGHT_LIST = [300, 350, 400, 450, 500]


class Bird:
    def __init__(self):
        self.y = WIN_HEIGHT // 2
        self.x = 75
        self.gravity = GRAVITY
        self.jumpSize = JUMPSIZE
        self.size = BIRD_SIZE
        self.color = BIRD_COLOR
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y += self.gravity
        self.gravity *= GRAVITY_INCREASE_RATE
        self.rect.y = self.y

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
        self.update_rects()

    def update_rects(self):
        self.rect1 = pygame.Rect(
            self.x, WIN_HEIGHT - self.height, self.width, self.height)
        self.rect2 = pygame.Rect(
            self.x, 0, self.width, WIN_HEIGHT - self.height - self.hole_size)

    def update(self):
        self.x -= self.movement
        self.update_rects()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect1)
        pygame.draw.rect(screen, self.color, self.rect2)


class FlappyBird:
    def __init__(self):
        self.winSize = (WIN_WIDTH, WIN_HEIGHT)
        self.screen = pygame.display.set_mode(self.winSize)
        pygame.display.set_caption("myFlappyBird")
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.running = True
        self.BLACK = BLACK
        self.bird = None
        self.pipes = []

        pygame.font.init()
        # Initialize font for score display
        self.font = pygame.font.Font(None, 36)

        self.restart()

    def spawn_pipe(self):
        height = random.choice(PIPE_HEIGHT_LIST)
        new_pipe = Pipe(WIN_WIDTH, height)
        self.pipes.append(new_pipe)

    def update_pipes(self):
        for pipe in self.pipes:
            pipe.update()
        if len(self.pipes) < 2 or self.pipes[0].x < -PIPE_WIDTH:
            self.pipes.pop(0)
            self.spawn_pipe()
            self.score += 1  # Increase score when a pipe is passed

    def restart(self):
        self.running = True
        self.fps = FPS
        self.bird = Bird()
        self.pipes = [
            Pipe(WIN_WIDTH, random.choice(PIPE_HEIGHT_LIST)),
            Pipe(WIN_WIDTH + WIN_WIDTH // 2, random.choice(PIPE_HEIGHT_LIST))
        ]
        self.score = 0  # Reset score when the game restarts

    def check_collision(self):
        if self.bird.y + self.bird.size > WIN_HEIGHT or self.bird.y < 0:
            return True
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect1) or self.bird.rect.colliderect(pipe.rect2):
                return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.bird.jump()
        elif keys[pygame.K_ESCAPE]:
            self.running = False

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        game_over_text = self.font.render(
            f"Game Over! Score: {self.score}", True, WHITE)
        continue_text = self.font.render("Continue? Y / N", True, WHITE)
        rect = pygame.Rect(WIN_WIDTH // 2 - 150,
                           WIN_HEIGHT // 2 - 100, 300, 200)
        pygame.draw.rect(self.screen, RED, rect)
        self.screen.blit(game_over_text, (rect.x + 20, rect.y + 50))
        self.screen.blit(continue_text, (rect.x + 20, rect.y + 100))

    def show_start_screen(self):
        start_text = self.font.render("Press S to Start", True, WHITE)
        self.screen.fill(BLACK)
        rect = pygame.Rect(WIN_WIDTH // 2 - 150,
                           WIN_HEIGHT // 2 - 50, 300, 100)
        pygame.draw.rect(self.screen, RED, rect)
        self.screen.blit(start_text, (rect.x + 30, rect.y + 30))
        pygame.display.update()

        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Start the game if 'S' is pressed
                        waiting_for_start = False
                    elif event.key == pygame.K_ESCAPE:  # Quit the game if 'ESCAPE' is pressed
                        self.running = False
                        pygame.quit()
                        return

    def run(self):
        self.show_start_screen()  # Show the start screen when the game first runs

        while self.running:
            self.handle_events()

            self.screen.fill(self.BLACK)
            self.bird.update()
            self.bird.draw(screen=self.screen)
            self.update_pipes()
            for pipe in self.pipes:
                pipe.draw(screen=self.screen)

            self.draw_score()  # Draw the score on the screen

            pygame.display.update()
            self.clock.tick(self.fps)

            if self.check_collision():
                self.draw_game_over()  # Show game over screen with score and continue prompt
                pygame.display.update()
                time.sleep(1)

                # Wait for user input
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:  # Continue if 'Y' is pressed
                                self.restart()
                                waiting_for_input = False
                                break
                            elif event.key == pygame.K_n:  # Quit if 'N' is pressed
                                self.running = False
                                waiting_for_input = False
                                pygame.quit()
                                return
                    time.sleep(0.1)


if __name__ == "__main__":
    fb = FlappyBird()
    fb.run()
