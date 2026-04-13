import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GREEN):
        super().__init__()
        # 创建平台精灵
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 平台属性
        self.is_moving = False
        self.move_speed = 2
        self.move_range = 100
        self.start_x = x
        self.start_y = y
        self.direction = 1
    
    def update(self):
        # 移动平台逻辑
        if self.is_moving:
            if self.rect.x < self.start_x - self.move_range or self.rect.x > self.start_x + self.move_range:
                self.direction *= -1
            self.rect.x += self.move_speed * self.direction
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)