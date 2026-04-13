import pygame
import random
from constants import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=RED):
        super().__init__()
        # 创建Boss精灵
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Boss属性
        self.speed_x = 3
        self.speed_y = 0
        self.health = 8
        self.attack_cooldown = 1000
        self.last_attack = 0
        self.direction = 1
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
    
    def attack(self, player):
        pass
    
    def ai_update(self, player):
        pass
    
    def move(self):
        pass
    
    def update(self, platforms, player):
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
        
        # AI更新
        self.ai_update(player)
        
        # 攻击
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > self.attack_cooldown:
            self.attack(player)
            self.last_attack = current_time
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class GoombaBoss(Boss):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 64, color=(0, 0, 0))
        # 创建卡通风格的板栗仔Boss
        self.image.set_colorkey((0, 0, 0))  # 设置黑色为透明
        
        # 绘制头部
        pygame.draw.circle(self.image, (0, 255, 0), (32, 32), 28)
        
        # 绘制眼睛
        pygame.draw.circle(self.image, (255, 255, 255), (24, 24), 6)
        pygame.draw.circle(self.image, (255, 255, 255), (40, 24), 6)
        pygame.draw.circle(self.image, (0, 0, 0), (24, 24), 3)
        pygame.draw.circle(self.image, (0, 0, 0), (40, 24), 3)
        
        # 绘制嘴巴
        pygame.draw.rect(self.image, (0, 0, 0), (24, 36, 16, 4))
        
        # 绘制手臂
        pygame.draw.circle(self.image, (0, 255, 0), (12, 32), 10)
        pygame.draw.circle(self.image, (0, 255, 0), (52, 32), 10)
        
        # 绘制腿
        pygame.draw.circle(self.image, (0, 255, 0), (24, 52), 10)
        pygame.draw.circle(self.image, (0, 255, 0), (40, 52), 10)
        
        self.health = 8
        self.attack_cooldown = 1500
        self.shielded = False
        self.shield_timer = 0
    
    def attack(self, player):
        # 随机选择攻击方式
        attack_type = random.randint(1, 3)
        if attack_type == 1:
            # 冲撞攻击
            if player.rect.x > self.rect.x:
                self.direction = 1
            else:
                self.direction = -1
            self.speed_x = 8
        elif attack_type == 2:
            # 跳跃砸击
            self.speed_y = -20
        elif attack_type == 3:
            # 召唤小怪
            from enemy import Mushroom
            return Mushroom(random.randint(100, 700), 100)
    
    def ai_update(self, player):
        # 护盾阶段
        if self.health <= 4 and not hasattr(self, 'shield_used'):
            self.shielded = True
            self.shield_timer = pygame.time.get_ticks()
            self.shield_used = True
        
        if self.shielded:
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_timer > 3000:
                self.shielded = False
        
        # 移动逻辑
        if abs(player.rect.x - self.rect.x) > 200:
            if player.rect.x > self.rect.x:
                self.direction = 1
            else:
                self.direction = -1
            self.rect.x += self.speed_x * self.direction

class BowserBoss(Boss):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, color=(0, 0, 0))
        # 创建卡通风格的酷霸王Boss
        self.image.set_colorkey((0, 0, 0))  # 设置黑色为透明
        
        # 绘制头部
        pygame.draw.circle(self.image, (139, 69, 19), (40, 30), 25)
        
        # 绘制角
        pygame.draw.polygon(self.image, (139, 69, 19), [(20, 15), (25, 5), (30, 15)])
        pygame.draw.polygon(self.image, (139, 69, 19), [(50, 15), (55, 5), (60, 15)])
        
        # 绘制眼睛
        pygame.draw.circle(self.image, (255, 255, 255), (32, 28), 5)
        pygame.draw.circle(self.image, (255, 255, 255), (48, 28), 5)
        pygame.draw.circle(self.image, (0, 0, 0), (32, 28), 3)
        pygame.draw.circle(self.image, (0, 0, 0), (48, 28), 3)
        
        # 绘制嘴巴
        pygame.draw.rect(self.image, (0, 0, 0), (30, 38, 20, 8))
        
        # 绘制身体
        pygame.draw.rect(self.image, (139, 69, 19), (20, 50, 40, 25))
        
        # 绘制手臂
        pygame.draw.rect(self.image, (139, 69, 19), (10, 50, 10, 15))
        pygame.draw.rect(self.image, (139, 69, 19), (60, 50, 10, 15))
        
        # 绘制腿
        pygame.draw.rect(self.image, (139, 69, 19), (25, 75, 10, 5))
        pygame.draw.rect(self.image, (139, 69, 19), (45, 75, 10, 5))
        
        self.health = 12
        self.attack_cooldown = 1000
        self.stage = 1
    
    def attack(self, player):
        # 根据阶段选择攻击方式
        if self.stage == 1:
            attack_type = random.randint(1, 2)
        elif self.stage == 2:
            attack_type = random.randint(1, 3)
        else:
            attack_type = random.randint(1, 4)
        
        if attack_type == 1:
            # 远程火球
            from bullet import Bullet
            return Bullet(self.rect.centerx, self.rect.centery, player.rect.x > self.rect.x)
        elif attack_type == 2:
            # 瞬移
            self.rect.x = random.randint(100, 700)
        elif attack_type == 3:
            # 冲刺攻击
            if player.rect.x > self.rect.x:
                self.direction = 1
            else:
                self.direction = -1
            self.speed_x = 10
        elif attack_type == 4:
            # 召唤岩浆
            pass
    
    def ai_update(self, player):
        # 阶段变化
        if self.health <= 8 and self.stage == 1:
            self.stage = 2
        elif self.health <= 4 and self.stage == 2:
            self.stage = 3
        
        # 移动逻辑
        if abs(player.rect.x - self.rect.x) > 300:
            if player.rect.x > self.rect.x:
                self.direction = 1
            else:
                self.direction = -1
            self.rect.x += self.speed_x * self.direction