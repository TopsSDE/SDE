import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 30
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("arial", 24)


class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy
        # Wrap around the screen
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2)

    def set_direction(self, dx, dy):
        self.dx = dx
        self.dy = dy


class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self):
        # Random movement for the ghost
        self.x += random.choice([-GRID_SIZE, 0, GRID_SIZE])
        self.y += random.choice([-GRID_SIZE, 0, GRID_SIZE])
        # Wrap around the screen
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, GRID_SIZE, GRID_SIZE))


class Game:
    def __init__(self):
        self.pacman = Pacman(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.ghosts = [
            Ghost(random.randint(0, SCREEN_WIDTH // GRID_SIZE) * GRID_SIZE,
                  random.randint(0, SCREEN_HEIGHT // GRID_SIZE) * GRID_SIZE, RED)
            for _ in range(3)
        ]
        self.dots = [
            (random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
             random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
            for _ in range(20)
        ]
        self.score = 0
        self.running = True

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, BLUE, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, BLUE, (0, y), (SCREEN_WIDTH, y))

    def draw_dots(self):
        for dot in self.dots:
            pygame.draw.circle(screen, WHITE, (dot[0] + GRID_SIZE // 2, dot[1] + GRID_SIZE // 2), GRID_SIZE // 6)

    def check_collisions(self):
        # Check if Pacman eats a dot
        for dot in self.dots[:]:
            if self.pacman.x == dot[0] and self.pacman.y == dot[1]:
                self.dots.remove(dot)
                self.score += 10

        # Check if Pacman hits a ghost
        for ghost in self.ghosts:
            if self.pacman.x == ghost.x and self.pacman.y == ghost.y:
                self.running = False

    def update(self):
        self.pacman.move()
        for ghost in self.ghosts:
            ghost.move()
        self.check_collisions()

    def render(self):
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_dots()
        self.pacman.draw()
        for ghost in self.ghosts:
            ghost.draw()

        # Display score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.set_direction(0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN:
                    self.pacman.set_direction(0, GRID_SIZE)
                elif event.key == pygame.K_LEFT:
                    self.pacman.set_direction(-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    self.pacman.set_direction(GRID_SIZE, 0)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()