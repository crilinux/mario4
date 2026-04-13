import pygame
from constants import *
from platform import Platform
from enemy import Mushroom, Turtle
from boss import GoombaBoss, BowserBoss
from item import Coin, Heart

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boss = None
        self.items = pygame.sprite.Group()
        self.background_color = WHITE
        
        # 加载关卡
        self.load_level()
    
    def load_level(self):
        if self.level_number == 1:
            self.load_level1()
        elif self.level_number == 2:
            self.load_level2()
    
    def load_level1(self):
        # 背景颜色
        self.background_color = (135, 206, 250)  # 天空蓝
        
        # 地面
        ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, color=(34, 139, 34))  # 绿色草地
        self.platforms.add(ground)
        
        # 平台
        platform1 = Platform(200, 400, 200, 20)
        platform2 = Platform(500, 300, 200, 20)
        platform3 = Platform(100, 200, 150, 20)
        platform3.is_moving = True
        self.platforms.add(platform1, platform2, platform3)
        
        # 敌人
        mushroom1 = Mushroom(300, 100)
        mushroom2 = Mushroom(600, 100)
        turtle = Turtle(400, 100)
        self.enemies.add(mushroom1, mushroom2, turtle)
        
        # Boss
        self.boss = GoombaBoss(400, 100)
        
        # 道具
        coin1 = Coin(250, 350)
        coin2 = Coin(550, 250)
        coin3 = Coin(150, 150)
        heart = Heart(400, 350)
        self.items.add(coin1, coin2, coin3, heart)
    
    def load_level2(self):
        # 背景颜色
        self.background_color = (0, 0, 139)  # 深蓝色洞穴
        
        # 地面
        ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, color=(139, 69, 19))  # 棕色砖块
        self.platforms.add(ground)
        
        # 平台
        platform1 = Platform(100, 400, 150, 20, color=(169, 169, 169))  # 金属平台
        platform2 = Platform(400, 300, 150, 20, color=(169, 169, 169))
        platform3 = Platform(700, 200, 100, 20, color=(169, 169, 169))
        platform2.is_moving = True
        self.platforms.add(platform1, platform2, platform3)
        
        # 敌人
        mushroom1 = Mushroom(200, 100)
        mushroom2 = Mushroom(500, 100)
        turtle1 = Turtle(300, 100)
        turtle2 = Turtle(600, 100)
        self.enemies.add(mushroom1, mushroom2, turtle1, turtle2)
        
        # Boss
        self.boss = BowserBoss(400, 100)
        
        # 道具
        coin1 = Coin(150, 350)
        coin2 = Coin(450, 250)
        coin3 = Coin(750, 150)
        heart1 = Heart(250, 350)
        heart2 = Heart(550, 250)
        self.items.add(coin1, coin2, coin3, heart1, heart2)
    
    def update(self, player):
        # 更新平台
        for platform in self.platforms:
            platform.update()
        
        # 更新敌人
        for enemy in self.enemies:
            enemy.update(self.platforms)
        
        # 更新Boss
        if self.boss:
            self.boss.update(self.platforms, player)
        
        # 更新道具
        for item in self.items:
            item.update()
    
    def draw(self, screen):
        # 绘制背景
        screen.fill(self.background_color)
        
        # 绘制平台
        for platform in self.platforms:
            platform.draw(screen)
        
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # 绘制Boss
        if self.boss:
            self.boss.draw(screen)
        
        # 绘制道具
        for item in self.items:
            item.draw(screen)