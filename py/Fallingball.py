# Importing necessary modules
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
GRADIENT_TOP = (135, 206, 235)
GRADIENT_BOTTOM = (173, 216, 230)

# Frames per second
FPS = 60

# Setting up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Object")

# Game clock
clock = pygame.time.Clock()


# Function to draw a gradient background
def draw_gradient():
    for i in range(SCREEN_HEIGHT):
        color = (
            GRADIENT_TOP[0] + (GRADIENT_BOTTOM[0] - GRADIENT_TOP[0]) * i // SCREEN_HEIGHT,
            GRADIENT_TOP[1] + (GRADIENT_BOTTOM[1] - GRADIENT_TOP[1]) * i // SCREEN_HEIGHT,
            GRADIENT_TOP[2] + (GRADIENT_BOTTOM[2] - GRADIENT_TOP[2]) * i // SCREEN_HEIGHT,
        )
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))


# Button class
class Button:
    def __init__(self, x, y, width, height, text, font_size=36):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.Font(None, font_size)

    def draw(self, surface, color=DARK_GRAY, text_color=WHITE):
        # Draw button rectangle
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height), border_radius=10)
        # Draw button text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height


# Basket class
class Basket:
    def __init__(self):
        self.width = 120
        self.height = 40
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 12

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height), border_radius=20)
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x + 10, self.y, self.width - 20, self.height - 20),
                         border_radius=15)


# Falling Object class
class FallingObject:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = 0
        self.speed = random.randint(4, 8)
        self.image = pygame.image.load("object.png")  # Replace with path to an actual image or use default shapes
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


# Main game function
def main():
    basket = Basket()  # Initialize the basket
    falling_objects = []  # List for falling objects
    score = 0  # Player's score
    lives = 5  # Number of lives
    running = True
    game_over = False

    while running:
        draw_gradient()

        # Handle all events properly
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Handle key presses for basket movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                basket.move("left")
            if keys[pygame.K_RIGHT]:
                basket.move("right")

            # Spawn new falling objects randomly
            if random.randint(1, 40) == 1:
                falling_objects.append(FallingObject())

            # Update and draw falling objects
            for obj in falling_objects[:]:  # Iterate over a copy of falling objects
                obj.fall()
                obj.draw(screen)

                # Handle object caught by basket
                if basket.y < obj.y + obj.size // 2 < basket.y + basket.height:
                    if basket.x < obj.x < basket.x + basket.width:
                        falling_objects.remove(obj)
                        score += 1

                # Handle object hitting the ground
                elif obj.y > SCREEN_HEIGHT:
                    falling_objects.remove(obj)
                    lives -= 1
                    if lives == 0:
                        game_over = True

            # Draw the basket
            basket.draw(screen)

            # Draw the score and lives text
            font = pygame.font.Font(None, 48)
            score_text = font.render(f"Score: {score}", True, BLACK)
            lives_text = font.render(f"Lives: {lives}", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))
        else:
            # Game over screen
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, BLACK)
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

            # Create and draw the Restart Button
            restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Restart", 36)
            restart_button.draw(screen, LIGHT_GRAY, BLACK)

            # Check if the restart button is clicked
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.is_clicked(pygame.mouse.get_pos()):
                        # Reset the game state without recursion
                        return main()

        # Update display
        pygame.display.flip()

        # Limit frames per second
        clock.tick(FPS)


if __name__ == "__main__":
    main()