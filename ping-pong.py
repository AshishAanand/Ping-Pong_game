import pygame as pg
import sys

# Initialize Pygame
pg.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Box dimensions
BOX_WIDTH = 50
BOX_HEIGHT = 20
PADDING = 5  # Spacing between boxes
ROWS = 5
INITIAL_COLS = 16  # Starting number of columns

box_list = []

# Screen setup
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
font = pg.font.SysFont(None, 55)

# Function to arrange boxes in a grid pattern, with dynamic columns
def arrange_boxes(cols):
    for row in range(ROWS):
        for col in range(cols):
            box_x = col * (BOX_WIDTH + PADDING)
            box_y = row * (BOX_HEIGHT + PADDING)
            box_list.append(pg.Rect(box_x, box_y, BOX_WIDTH, BOX_HEIGHT))

# Function to reset the game state
def reset_game():
    global player_rect, ball_rect, ball_speed, box_list, cols
    player_rect = pg.Rect(350, 550, 100, 10)
    ball_rect = pg.Rect(400, 540, 20, 20)  # Circle's radius is 10
    ball_speed = [5, -5]  # Initial ball speed in x and y directions
    box_list = []
    arrange_boxes(cols)  # Reset the boxes with the current column count

# Function to display a restart message
def show_restart_message():
    message = font.render("You missed! Press any key to restart", True, WHITE)
    screen.blit(message, (100, 250))
    pg.display.update()
    
    # Wait for key press to restart the game
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                waiting = False

# Function to handle ball and board movements
def main_game(player_rect, ball_rect, ball_speed):
    global cols

    # Handle events (like quitting the game)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Get key state and update player position
    keys = pg.key.get_pressed()
    if keys[pg.K_a] and player_rect.left > 0:  # Move left
        player_rect.x -= 5
    if keys[pg.K_d] and player_rect.right < SCREEN_WIDTH:  # Move right
        player_rect.x += 5

    # Ball movement
    ball_rect.x += ball_speed[0]
    ball_rect.y += ball_speed[1]

    # Ball collision with walls
    if ball_rect.left <= 0 or ball_rect.right >= SCREEN_WIDTH:
        ball_speed[0] = -ball_speed[0]  # Reverse horizontal direction
    if ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]  # Reverse vertical direction

    # Ball collision with player (board)
    if ball_rect.colliderect(player_rect):
        # Calculate hit position on the board
        hit_pos = (ball_rect.centerx - player_rect.left) / player_rect.width
        ball_speed[0] = (hit_pos - 0.5) * 10  # Adjust horizontal speed based on where the ball hits the board
        ball_speed[1] = -ball_speed[1]  # Reverse vertical direction

    # Ball collision with boxes
    for box in box_list[:]:
        if ball_rect.colliderect(box):
            box_list.remove(box)  # Remove box on collision
            ball_speed[1] = -ball_speed[1]  # Reverse vertical direction
            break

    # Check if all boxes are destroyed
    if not box_list:
        cols += 2  # Increase the number of columns for new boxes
        arrange_boxes(cols)  # Recreate boxes with extra columns

    # Check if the ball falls below the screen (i.e., player misses the ball)
    if ball_rect.top > SCREEN_HEIGHT:
        show_restart_message()
        reset_game()  # Reset the game when the player misses the ball

    # Clear screen
    screen.fill(BLACK)

    # Draw player (board)
    pg.draw.rect(screen, RED, player_rect)

    # Draw ball
    pg.draw.circle(screen, WHITE, ball_rect.center, ball_rect.width // 2)

    # Draw boxes
    for box in box_list:
        pg.draw.rect(screen, GREEN, box)

    pg.display.update()

# Initialize player (board) and ball
cols = INITIAL_COLS  # Start with initial column count
reset_game()

# Game loop
while True:
    main_game(player_rect, ball_rect, ball_speed)
    clock.tick(60)  # Limit to 60 FPS
