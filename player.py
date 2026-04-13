import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 创建卡通风格的玩家精灵
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.set_colorkey((0, 0, 0))  # 设置黑色为透明
        
        # 绘制头部
        pygame.draw.circle(self.image, (255, 204, 153), (16, 12), 10)
        
        # 绘制帽子
        pygame.draw.rect(self.image, (255, 0, 0), (6, 2, 20, 10))
        pygame.draw.circle(self.image, (255, 0, 0), (16, 2), 6)
        
        # 绘制眼睛
        pygame.draw.circle(self.image, (255, 255, 255), (12, 10), 2)
        pygame.draw.circle(self.image, (255, 255, 255), (20, 10), 2)
        pygame.draw.circle(self.image, (0, 0, 0), (12, 10), 1)
        pygame.draw.circle(self.image, (0, 0, 0), (20, 10), 1)
        
        # 绘制身体
        pygame.draw.rect(self.image, (0, 0, 255), (8, 22, 16, 20))
        
        # 绘制手臂
        pygame.draw.rect(self.image, (255, 204, 153), (4, 22, 4, 12))
        pygame.draw.rect(self.image, (255, 204, 153), (24, 22, 4, 12))
        
        # 绘制腿
        pygame.draw.rect(self.image, (139, 69, 19), (10, 42, 6, 6))
        pygame.draw.rect(self.image, (139, 69, 19), (16, 42, 6, 6))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 玩家属性
        self.speed_x = 0
        self.speed_y = 0
        self.jump_count = 0
        self.max_jumps = 2  # 允许二段跳
        self.health = 10
        self.facing_right = True
        self.invincible = False
        self.invincible_timer = 0
        
    def move(self, dx):
        self.speed_x = dx * PLAYER_SPEED
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False
    
    def jump(self):
        if self.jump_count < self.max_jumps:
            self.speed_y = PLAYER_JUMP_POWER
            self.jump_count += 1
    
    def attack(self, bullets):
        # 发射火球
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.facing_right)
        bullets.add(bullet)
    
    def update(self, platforms):
        # 检查无敌状态
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_timer > 3000:
                self.invincible = False
        
        # 应用重力
        self.speed_y += GRAVITY
        
        # 水平移动
        self.rect.x += self.speed_x
        
        # 碰撞检测（水平）
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.speed_x > 0:
                    self.rect.right = platform.rect.left
                elif self.speed_x < 0:
                    self.rect.left = platform.rect.right
        
        # 垂直移动
        self.rect.y += self.speed_y
        
        # 碰撞检测（垂直）
        on_ground = False
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.speed_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.speed_y = 0
                    self.jump_count = 0
                    on_ground = True
                elif self.speed_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.speed_y = 0
        
        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 导入bullet模块，避免循环导入
from bullet import Bullet