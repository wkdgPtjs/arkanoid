import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
window_width = 800
window_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Paddle dimensions
paddle_width = 100
paddle_height = 20

# Ball dimensions and initial speed
initial_ball_radius = 7
ball_speed_x = 5
ball_speed_y = -3

# Maximum ball size
max_ball_radius = 130

# Brick dimensions
brick_width = 80
brick_height = 20

# Number of bricks
num_bricks = 50

# Create the game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Brick Breaker")

clock = pygame.time.Clock()

# Create the paddle
paddle = pygame.Rect(window_width // 2 - paddle_width // 2, window_height - paddle_height - 10, paddle_width,
                     paddle_height)

# Create the ball
ball_radius = initial_ball_radius
ball = pygame.Rect(window_width // 2 - ball_radius, window_height // 2 - ball_radius, ball_radius * 2, ball_radius * 2)

# Create bricks
bricks = []
for i in range(num_bricks):
    brick = pygame.Rect((i % 10) * (brick_width + 5), (i // 10) * (brick_height + 5) + 50, brick_width, brick_height)
    bricks.append(brick)

# Initialize ball direction
ball_direction = [random.choice([-1, 1]), -1]

# Game loop variables
game_over = False
restart = False
exit_game = False

# Buttons
restart_button = pygame.Rect(window_width // 2 - 75, window_height // 2 - 25, 150, 50)
exit_button = pygame.Rect(window_width // 2 - 75, window_height // 2 + 50, 150, 50)
# Button colors
restart_button_color = white
exit_button_color = white
button_text_color = black

# Paddle speed
paddle_speed = 10  # Adjust this value to increase the paddle speed

# Game loop
while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    restart = True
                elif exit_button.collidepoint(mouse_pos):
                    exit_game = True

    if restart:
        restart = False
        game_over = False
        bricks = []
        for i in range(num_bricks):
            brick = pygame.Rect((i % 10) * (brick_width + 5), (i // 10) * (brick_height + 5) + 50, brick_width,
                                brick_height)
            bricks.append(brick)
        paddle.x = window_width // 2 - paddle_width // 2
        ball.x = window_width // 2 - ball_radius
        ball.y = window_height // 2 - ball_radius
        ball_radius = initial_ball_radius
        ball = pygame.Rect(ball.x, ball.y, ball_radius * 2, ball_radius * 2)
        ball_direction = [random.choice([-1, 1]), -1]

    if not game_over:
        # Move the paddle with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT]:
            paddle.x += paddle_speed

        # Update ball position
        ball.x += ball_speed_x * ball_direction[0]
        ball.y += ball_speed_y * ball_direction[1]

        # Collision detection - ball and walls
        if ball.left <= 0 or ball.right >= window_width:
            ball_direction[0] *= -1
        if ball.top <= 0:
            ball_direction[1] *= -1

        # Collision detection - ball and paddle
        if ball.colliderect(paddle):
            ball_direction[1] *= -1

        # Collision detection - ball and bricks
        for brick in bricks:
            if ball.colliderect(brick):
                ball_direction[1] *= -1
                bricks.remove(brick)
                if ball_radius < max_ball_radius:
                    ball_radius += 5  # Increase the ball radius by 5
                    ball = pygame.Rect(ball.x, ball.y, ball_radius * 2, ball_radius * 2)
                break

        # Check if all bricks are broken - win condition
        if len(bricks) == 0:
            game_over = "win"

        # Check if the ball hits the bottom wall - game over
        if ball.bottom >= window_height:
            game_over = "lose"

    # Clear the window
    window.fill(black)

    # Draw the paddle
    pygame.draw.rect(window, blue, paddle)

    # Draw the ball
    pygame.draw.circle(window, red, (ball.x + ball_radius, ball.y + ball_radius), ball_radius)

    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(window, green, brick)

    # Draw buttons and messages
    if game_over:
        pygame.draw.rect(window, restart_button_color, restart_button)
        pygame.draw.rect(window, exit_button_color, exit_button)
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Restart", True, button_text_color)
        exit_text = font.render("Exit", True, button_text_color)
        win_text = font.render("WIN!", True, green)
        lose_text = font.render("GAME OVER", True, red)

        restart_text_pos = (restart_button.x + restart_button.width // 2 - restart_text.get_width() // 2,
                            restart_button.y + restart_button.height // 2 - restart_text.get_height() // 2)
        exit_text_pos = (exit_button.x + exit_button.width // 2 - exit_text.get_width() // 2,
                         exit_button.y + exit_button.height // 2 - exit_text.get_height() // 2)
        win_text_pos = (window_width // 2 - win_text.get_width() // 2, window_height // 2 - win_text.get_height() // 2 - 40)
        lose_text_pos = (window_width // 2 - lose_text.get_width() // 2, window_height // 2 - lose_text.get_height() // 2 - 40)

        window.blit(restart_text, restart_text_pos)
        window.blit(exit_text, exit_text_pos)
        if game_over == "win":
            window.blit(win_text, win_text_pos)
        else:
            window.blit(lose_text, lose_text_pos)

    # Update the window
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Quit the game
pygame.quit()
