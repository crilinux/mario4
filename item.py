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
    
    def draw(self, screen):
        # 绘制圆形的黄色铜币
        pygame.draw.circle(screen, YELLOW, (self.rect.x + 10, self.rect.y + 10), 10)
        # 绘制铜币的细节
        pygame.draw.circle(screen, (255, 200, 0), (self.rect.x + 10, self.rect.y + 10), 8)
        pygame.draw.circle(screen, YELLOW, (self.rect.x + 10, self.rect.y + 10), 6)

class Heart(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, color=RED)
        self.value = 1