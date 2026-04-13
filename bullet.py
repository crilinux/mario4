import pygame
from constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        # 创建子弹精灵（使用颜色块代替）
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # 子弹属性
        self.speed_x = BULLET_SPEED if facing_right else -BULLET_SPEED
        self.speed_y = 0
    
    def update(self):
        # 移动子弹
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # 边界检查
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)