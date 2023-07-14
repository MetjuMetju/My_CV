import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
playground_width = 10
playground_height = 20
block_size = 30
playground_offset_x = (screen_width - playground_width * block_size) // 2
playground_offset_y = screen_height - playground_height * block_size

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define Tetris shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
]

# Initialize the playground grid
playground = [[0] * playground_width for _ in range(playground_height)]

# Initialize the current block
current_block = random.choice(shapes)
current_block_x = playground_width // 2 - len(current_block[0]) // 2
current_block_y = 0

# Initialize the score
score = 0

# Initialize the block's falling speed
fall_speed = 1
fall_speed_increase = 0.2

# Check if a block can be placed at the specified position
def can_place_block(block, x, y):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if (
                block[row][col] != 0
                and (
                    x + col < 0
                    or x + col >= playground_width
                    or y + row >= playground_height
                    or playground[y + row][x + col] != 0
                )
            ):
                return False
    return True

# Place the current block on the playground
def place_block(block, x, y):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col] != 0:
                playground[y + row][x + col] = 1

# Rotate the current block
def rotate_block(block):
    return list(zip(*block[::-1]))

# Check if a line is full
def is_line_full(line):
    for cell in line:
        if cell == 0:
            return False
    return True

# Clear a full line
def clear_line(line):
    for i in range(line, 0, -1):
        playground[i] = playground[i - 1].copy()
    playground[0] = [0] * playground_width

# Clear all full lines
def clear_full_lines():
    lines_cleared = 0
    for i in range(playground_height):
        if is_line_full(playground[i]):
            clear_line(i)
            lines_cleared += 1
    return lines_cleared

# Draw the playground grid
def draw_playground():
    for row in range(playground_height):
        for col in range(playground_width):
            cell_color = WHITE if playground[row][col] == 1 else BLACK
            pygame.draw.rect(
                screen,
                cell_color,
                (
                    playground_offset_x + col * block_size,
                    playground_offset_y + row * block_size,
                    block_size,
                    block_size,
                ),
            )

# Draw the current block
def draw_current_block():
    for row in range(len(current_block)):
        for col in range(len(current_block[row])):
            if current_block[row][col] != 0:
                cell_color = BLUE
                pygame.draw.rect(
                    screen,
                    cell_color,
                    (
                        playground_offset_x + (current_block_x + col) * block_size,
                        playground_offset_y + (current_block_y + row) * block_size,
                        block_size,
                        block_size,
                    ),
                )

# Draw the score
def draw_score():
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(text, (10, 10))

# Game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if can_place_block(current_block, current_block_x - 1, current_block_y):
                    current_block_x -= 1
            elif event.key == pygame.K_RIGHT:
                if can_place_block(current_block, current_block_x + 1, current_block_y):
                    current_block_x += 1
            elif event.key == pygame.K_DOWN:
                if can_place_block(current_block, current_block_x, current_block_y + 1):
                    current_block_y += 1
            elif event.key == pygame.K_SPACE:
                rotated_block = rotate_block(current_block)
                if can_place_block(rotated_block, current_block_x, current_block_y):
                    current_block = rotated_block
            elif event.key == pygame.K_UP:
                fall_speed += fall_speed_increase

    # Move the current block down
    if can_place_block(current_block, current_block_x, current_block_y + 1):
        current_block_y += 1
    else:
        place_block(current_block, current_block_x, current_block_y)
        lines_cleared = clear_full_lines()
        score += lines_cleared * 10

        # Adjust the falling speed based on lines cleared
        if lines_cleared > 0:
            fall_speed += fall_speed_increase

        current_block = random.choice(shapes)
        current_block_x = playground_width // 2 - len(current_block[0]) // 2
        current_block_y = 0
        if not can_place_block(current_block, current_block_x, current_block_y):
            game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw the playground
    draw_playground()

    # Draw the current block
    draw_current_block()

    # Draw the score
    draw_score()

    # Update the display
    pygame.display.flip()

    # Set the frame rate based on falling speed
    clock.tick(fall_speed)

# Game over
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(BLACK)

    # Display the game over message
    font = pygame.font.SysFont(None, 50)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()
