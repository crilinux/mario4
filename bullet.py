import pygame
from constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right, owner='player'):
        super().__init__()
        # 创建子弹精灵（使用颜色块代替）
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        # 添加子弹的细节
        pygame.draw.circle(self.image, (255, 100, 100), (15, 15), 12)
        pygame.draw.circle(self.image, (255, 200, 200), (15, 15), 6)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # 子弹属性
        self.speed_x = BULLET_SPEED if facing_right else -BULLET_SPEED
        self.speed_y = 0
        self.owner = owner
        
        # 打印初始位置（仅在开发阶段使用）
        # print(f"子弹初始位置: ({self.rect.x}, {self.rect.y})")
    
    def update(self):
        # 移动子弹
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # 打印移动后的位置（仅在开发阶段使用）
        # print(f"子弹移动位置: ({self.rect.x}, {self.rect.y})")
        
        # 边界检查
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right, owner='boss'):
        super().__init__()
        # 创建火球精灵
        self.image = pygame.Surface((40, 40))
        self.image.fill(ORANGE)
        # 添加火球的细节
        pygame.draw.circle(self.image, YELLOW, (20, 20), 16)
        pygame.draw.circle(self.image, (255, 150, 0), (20, 20), 8)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # 火球属性
        self.speed_x = BULLET_SPEED * 0.5 if facing_right else -BULLET_SPEED * 0.6
        self.speed_y = 0
        self.owner = owner
        
        # 打印初始位置和速度（仅在开发阶段使用）
        print(f"火球初始位置: ({self.rect.x}, {self.rect.y}), 速度: {self.speed_x}, facing_right: {facing_right}, owner: {owner}")
    
    def update(self):
        # 移动火球
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # 打印移动后的位置（仅在开发阶段使用）
        print(f"火球移动位置: ({self.rect.x}, {self.rect.y})")
        
        # 边界检查
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)