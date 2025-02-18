import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Pentagon and Bouncy Ball")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Clock and Time control
clock = pygame.time.Clock()
FPS = 60

# Pentagon properties
PENTAGON_RADIUS = 200
PENTAGON_CENTER = (WIDTH // 2, HEIGHT // 2)
ROTATION_SPEED = 0.02  # radians per frame

# Ball properties
BALL_RADIUS = 10
ball_pos = [PENTAGON_CENTER[0], PENTAGON_CENTER[1] - 100]  # Start inside the pentagon
ball_velocity = [0, 0]

# Physics constants
GRAVITY = 0.5
FRICTION = 0.98  # Reduces velocity after collisions but keeps it near 1 for a bouncier effect
BOUNCINESS = 1.1  # Add extra velocity after a collision for "bouncier" effect


# Function to calculate pentagon vertices
def calculate_pentagon(center, radius, angle_offset=0):
    vertices = []
    for i in range(5):
        angle = angle_offset + i * (2 * math.pi / 5)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices


# Check if a point is near a line segment (used for collision detection)
def point_to_line_distance(px, py, x1, y1, x2, y2):
    # Vector calculations to find perpendicular distance
    edge_length_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if edge_length_squared == 0:
        return math.hypot(px - x1, py - y1)

    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / edge_length_squared))
    nearest_x = x1 + t * (x2 - x1)
    nearest_y = y1 + t * (y2 - y1)
    return math.hypot(px - nearest_x, py - nearest_y), nearest_x, nearest_y


# Function to reflect ball velocity when it hits the walls
def reflect_ball(ball_pos, ball_velocity, vertices):
    px, py = ball_pos

    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]

        # Check if the ball is close enough to the edge
        distance, nearest_x, nearest_y = point_to_line_distance(px, py, x1, y1, x2, y2)

        if distance <= BALL_RADIUS:
            # Reflect velocity using the edge's normal vector
            edge_dx = x2 - x1
            edge_dy = y2 - y1
            edge_length = math.hypot(edge_dx, edge_dy)
            normal_dx = -edge_dy / edge_length
            normal_dy = edge_dx / edge_length

            dot_product = ball_velocity[0] * normal_dx + ball_velocity[1] * normal_dy
            ball_velocity[0] -= 2 * dot_product * normal_dx
            ball_velocity[1] -= 2 * dot_product * normal_dy

            # Amplify the velocity slightly for bounciness
            ball_velocity[0] *= BOUNCINESS
            ball_velocity[1] *= BOUNCINESS

            # Reposition ball to prevent it from getting stuck in the wall
            overlap = BALL_RADIUS - distance
            ball_pos[0] += normal_dx * overlap
            ball_pos[1] += normal_dy * overlap
            return


# Main game loop
running = True
angle = 0  # Initial rotation angle of the pentagon
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Update pentagon rotation
    angle += ROTATION_SPEED
    pentagon_vertices = calculate_pentagon(PENTAGON_CENTER, PENTAGON_RADIUS, angle)

    # Draw the rotating pentagon
    pygame.draw.polygon(screen, BLUE, pentagon_vertices, 3)

    # Apply gravity to the ball
    ball_velocity[1] += GRAVITY

    # Update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Handle collisions with the pentagon walls
    reflect_ball(ball_pos, ball_velocity, pentagon_vertices)

    # Reduce velocity slightly to simulate friction and avoid infinite bouncing
    ball_velocity[0] *= FRICTION
    ball_velocity[1] *= FRICTION

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
