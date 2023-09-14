import pygame
import sys

# 初始化 Pygame
pygame.init()

# 游戏窗口设置
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simple RPG Game")

# 角色设置
player_image = pygame.Surface((50, 50))
player_image.fill((0, 255, 0))
player_rect = player_image.get_rect()
player_rect.center = (window_size[0] // 2, window_size[1] // 2)

# 游戏循环
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 处理角色移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        player_rect.y += 5
    
    # 绘制角色和背景
    screen.fill((0, 0, 0))
    screen.blit(player_image, player_rect)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()