import pygame
import random

"""
*
* Please read this
* Instructions
* Use joystick axis or keyboard arrow keys
* Press A in joystick or R in keyboard to restart when game over
* Press B in joystick or Q in keyboard to quit
*
"""

pygame.init()

# Window dimensions
window_width = 800
window_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Snake and apple sizes
snake_size = 10
apple_size = 10

# Snake movement speed
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Game window
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

# Function to display the score
def display_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    game_window.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_window, white, [pixel[0], pixel[1], snake_size, snake_size])

# Main game loop
def game_loop():
    game_over = False
    game_exit = False

    # Snake's initial position
    x1 = window_width / 2
    y1 = window_height / 2

    # Snake's initial movement direction
    x1_change = 0
    y1_change = 0

    # Snake's initial length
    snake_pixels = []
    snake_length = 1

    # Apple's initial position
    apple_x = round(random.randrange(0, window_width - apple_size) / 10.0) * 10.0
    apple_y = round(random.randrange(0, window_height - apple_size) / 10.0) * 10.0

    # Initialize joystick
    pygame.joystick.init()
    init = pygame.joystick.get_count() > 0
    if init:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    # Game loop
    while not game_exit:
        while game_over:
            game_window.fill(black)
            message = font_style.render(f"Game Over!", True, red)
            game_window.blit(message, [window_width / 3, window_height / 3])
            display_score(snake_length - 1)
            pygame.display.update()

            # Prompt to play again or quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        game_exit = True
                    if event.key == pygame.K_r:
                        game_loop()
                if pygame.joystick.get_count() > 0:
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0:  # A button
                            game_over = False
                            game_exit = False
                            game_loop()
                        elif event.button == 1: # B button
                            game_over = False
                            game_exit = True
        
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if pygame.joystick.get_count() > 0:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1: # B button
                        game_over = False
                        game_exit = True

        # Check joystick input
        if pygame.joystick.get_count() > 0:
            axes = joystick.get_numaxes()
            for i in range(axes):
                axis = joystick.get_axis(i)
                if i == 0:  # X-axis
                    if axis < -0.5:
                        x1_change = -snake_size
                        y1_change = 0
                    elif axis > 0.5:
                        x1_change = snake_size
                        y1_change = 0
                elif i == 1:  # Y-axis
                    if axis < -0.5:
                        y1_change = -snake_size
                        x1_change = 0
                    elif axis > 0.5:
                        y1_change = snake_size
                        x1_change = 0

        # Check if the snake hits the boundaries of the game window
        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_over = True

        # Update the snake's position
        x1 += x1_change
        y1 += y1_change

        # Clear the game window
        game_window.fill(black)

        # Draw the apple
        pygame.draw.rect(game_window, red, [apple_x, apple_y, apple_size, apple_size])

        # Update the snake's length and position
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_pixels.append(snake_head)
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

        # Check if the snake collides with itself
        for pixel in snake_pixels[:-1]:
            if pixel == snake_head:
                game_over = True

        # Draw the snake
        draw_snake(snake_size, snake_pixels)

        # Check if the snake eats the apple
        if x1 == apple_x and y1 == apple_y:
            apple_x = round(random.randrange(0, window_width - apple_size) / 10.0) * 10.0
            apple_y = round(random.randrange(0, window_height - apple_size) / 10.0) * 10.0
            snake_length += 1

        # Display the score
        display_score(snake_length - 1)

        # Refresh the game window
        pygame.display.update()

        # Set the snake's movement speed
        pygame.time.Clock().tick(snake_speed)

    # Quit Pygame
    pygame.quit()

# Start the game loop
game_loop()
