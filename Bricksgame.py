import pygame
import random

pygame.init()

window_width = 500
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Brick Breaker")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

paddle_width = 100
paddle_height = 10
paddle_x = window_width // 2 - paddle_width // 2
paddle_y = window_height - 50
paddle_speed = 5

ball_radius = 10
ball_x = window_width // 2
ball_y = paddle_y - ball_radius
ball_speed_x = 3
ball_speed_y = -3

brick_width = 70
brick_height = 20
nrows = 1
nbricksrow = 5
maxbricks = nrows * nbricksrow 
brickcolors = [RED, GREEN, BLUE, YELLOW, ORANGE]

bricks = []
for row in range(nrows):
    for brick in range(nbricksrow):
        brick_x = brick * (brick_width + 5) + 60
        brick_y = row * (brick_height + 5) + 100
        brick_color = random.choice(brickcolors)
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

lives = 3
score = 0
level = 1
brick_increment = 1 
game_over = False

clock = pygame.time.Clock()

def generate_bricks():
    bricks.clear()
    for row in range(nrows + level - 1):
        for brick in range(nbricksrow):
            brick_x = brick * (brick_width + 5) + 60
            brick_y = row * (brick_height + 5) + 130
            brick_color = random.choice(brickcolors)
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < window_width - paddle_width:
        paddle_x += paddle_speed

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_x <= 0 or ball_x >= window_width - ball_radius:
        ball_speed_x *= -1
    if ball_y <= 0:
        ball_speed_y *= -1

    if pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height).colliderect(
            pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
    ):
      ball_speed_y *= -1

    for brick in bricks:
        if pygame.Rect(brick).colliderect(
            pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        ):
            ball_speed_y *= -1
            bricks.remove(brick)
            score += 10

    if ball_y >= window_height:
        lives -= 1
        if lives == 0:
            game_over = True
        else:
            ball_x = window_width // 2
            ball_y = paddle_y - ball_radius

    if len(bricks) == 0:
        level += 1
        brick_increment += 1
        generate_bricks()
        ball_x = window_width // 2
        ball_y = paddle_y - ball_radius

    window.fill(WHITE)


    pygame.draw.rect(window, BLACK, (paddle_x, paddle_y, paddle_width, paddle_height))

    pygame.draw.circle(window, BLACK, (ball_x, ball_y), ball_radius)

    for brick in bricks:
        pygame.draw.rect(window, brickcolors[random.randint(0, len(brickcolors) - 1)], brick)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (window_width - lives_text.get_width() - 10, 10))
   

    pygame.display.flip()

   
    clock.tick(60)


font = pygame.font.Font(None, 72)
game_over_text = font.render("Game Over", True, BLACK)
window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

pygame.time.wait(3000)

pygame.quit()

