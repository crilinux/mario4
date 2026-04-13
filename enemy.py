import pygame
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=RED):
        super().__init__()
        # 创建敌人精灵
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 敌人属性
        self.speed_x = ENEMY_SPEED
        self.speed_y = 0
        self.health = 1
        self.direction = 1
    
    def update(self, platforms):
        # 移动敌人
        self.rect.x += self.speed_x * self.direction
        
        # 碰撞检测（水平）
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.direction > 0:
                    self.rect.right = platform.rect.left
                elif self.direction < 0:
                    self.rect.left = platform.rect.right
                self.direction *= -1
        
        # 边界检查
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
        
        # 应用重力
        self.speed_y += GRAVITY
        self.rect.y += self.speed_y
        
        # 碰撞检测（垂直）
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.speed_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.speed_y = 0
                elif self.speed_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.speed_y = 0
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Mushroom(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, color=(0, 0, 0))
        # 创建卡通风格的蘑菇怪
        self.image.set_colorkey((0, 0, 0))  # 设置黑色为透明
        
        # 绘制蘑菇帽
        pygame.draw.circle(self.image, (255, 0, 0), (16, 12), 12)
        
        # 绘制蘑菇茎
        pygame.draw.rect(self.image, (255, 204, 153), (12, 24, 8, 8))
        
        # 绘制眼睛
        pygame.draw.circle(self.image, (255, 255, 255), (12, 10), 3)
        pygame.draw.circle(self.image, (255, 255, 255), (20, 10), 3)
        pygame.draw.circle(self.image, (0, 0, 0), (12, 10), 1)
        pygame.draw.circle(self.image, (0, 0, 0), (20, 10), 1)

class Turtle(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, color=(0, 0, 0))
        # 创建卡通风格的乌龟
        self.image.set_colorkey((0, 0, 0))  # 设置黑色为透明
        
        # 绘制龟壳
        pygame.draw.rect(self.image, (139, 69, 19), (4, 8, 24, 16))
        pygame.draw.rect(self.image, (101, 67, 33), (8, 12, 16, 8))
        
        # 绘制头部
        pygame.draw.circle(self.image, (139, 69, 19), (8, 16), 4)
        
        # 绘制腿
        pygame.draw.rect(self.image, (139, 69, 19), (4, 24, 4, 4))
        pygame.draw.rect(self.image, (139, 69, 19), (12, 24, 4, 4))
        pygame.draw.rect(self.image, (139, 69, 19), (20, 24, 4, 4))
        pygame.draw.rect(self.image, (139, 69, 19), (28, 24, 4, 4))
        
        # 绘制眼睛
        pygame.draw.circle(self.image, (255, 255, 255), (6, 14), 1)
        pygame.draw.circle(self.image, (0, 0, 0), (6, 14), 0.5)
        self.shelled = False