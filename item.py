import pygame
from constants import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=YELLOW):
        super().__init__()
        # 创建道具精灵
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 道具属性
        self.value = 1
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Coin(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, color=YELLOW)
        self.value = 10

class Heart(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, color=RED)
        self.value = 1