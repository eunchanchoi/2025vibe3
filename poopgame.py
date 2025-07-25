import pygame
import random


# Initialize game
pygame.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid the Poop")

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLUE = (0, 102, 204)



# Load images (fallback to rectangles if not found)
player_size = 60   # Make cat image smaller
poop_size = 50     # Make poop image smaller than cat
import os
# 이미지 경로를 배경화면 폴더로 지정 (예시: C:\Users\USER\Pictures\배경화면)
cat_img_path = r"C:\Users\USER\Pictures\배경화면\cat.png"
poop_img_path = r"C:\Users\USER\Pictures\배경화면\poop.png"
try:
    cat_img = pygame.image.load(cat_img_path).convert_alpha()
    cat_img = pygame.transform.scale(cat_img, (player_size, player_size))
except Exception:
    cat_img = None
try:
    poop_img = pygame.image.load(poop_img_path).convert_alpha()
    poop_img = pygame.transform.scale(poop_img, (poop_size, poop_size))
except Exception:
    poop_img = None
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT - player_size - 10
player_speed = 7
poop_speed = 7  # Make poop fall faster
poop_speed_increase = 0  # No speed increase
poop_x = random.randint(0, SCREEN_WIDTH - poop_size)
poop_y = -poop_size

# Score
score = 0

# Font
font = pygame.font.SysFont(None, 36)


# Game loop with restart
def reset_game():
    global player_x, player_y, poop_speed, poop_x, poop_y, score
    player_x = SCREEN_WIDTH // 2 - player_size // 2
    player_y = SCREEN_HEIGHT - player_size - 10
    poop_speed = 7
    poop_x = random.randint(0, SCREEN_WIDTH - poop_size)
    poop_y = -poop_size
    score = 0

clock = pygame.time.Clock()
while True:
    reset_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
            player_x += player_speed

        # Move and respawn poop
        poop_y += poop_speed
        if poop_y > SCREEN_HEIGHT:
            poop_y = -poop_size
            poop_x = random.randint(0, SCREEN_WIDTH - poop_size)
            score += 1
            poop_speed += 0.5  # Increase speed for difficulty

        # Collision check
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        poop_rect = pygame.Rect(poop_x, poop_y, poop_size, poop_size)
        if player_rect.colliderect(poop_rect):
            running = False

        # Draw screen
        screen.fill(WHITE)
        if cat_img:
            screen.blit(cat_img, (player_x, player_y))
        else:
            pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
        if poop_img:
            screen.blit(poop_img, (poop_x, poop_y))
        else:
            pygame.draw.rect(screen, BROWN, (poop_x, poop_y, poop_size, poop_size))
        score_text = font.render(f"Score: {score}", True, (0,0,0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    # Game over message with restart button
    screen.fill(WHITE)
    over_text = font.render(f"Game Over! Score: {score}", True, (255,0,0))
    button_font = pygame.font.SysFont(None, 48)
    button_text = button_font.render("Restart", True, (255,255,255))
    button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 60, 200, 60)
    pygame.draw.rect(screen, (0, 102, 204), button_rect)
    screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width())//2, button_rect.y + (button_rect.height - button_text.get_height())//2))
    pygame.display.flip()
    # Wait for restart button click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False
