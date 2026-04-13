import pygame
import pygame.sndarray
import numpy as np
import math
from constants import *
from player import Player
from level import Level
from item import Coin, Heart

class Game:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        pygame.mixer.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Platformer Adventure")
        
        # 游戏时钟
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.current_state = GAME_STATE['menu']
        
        # 游戏变量
        self.current_level = 1
        self.player = None
        self.level = None
        self.bullets = pygame.sprite.Group()
        self.score = 0
        
        # 生成音效
        self.sounds = {}
        try:
            # 生成跳跃音效
            jump_data = np.array([int(32767 * math.sin(2 * math.pi * 440 * i / 44100)) for i in range(44100 // 10)], dtype=np.int16)
            jump_stereo = np.column_stack((jump_data, jump_data))  # 转换为立体声音频
            jump_sound = pygame.sndarray.make_sound(jump_stereo)
            self.sounds['jump'] = jump_sound
            
            # 生成攻击音效
            attack_data = np.array([int(32767 * math.sin(2 * math.pi * 880 * i / 44100)) for i in range(44100 // 20)], dtype=np.int16)
            attack_stereo = np.column_stack((attack_data, attack_data))  # 转换为立体声音频
            attack_sound = pygame.sndarray.make_sound(attack_stereo)
            self.sounds['attack'] = attack_sound
            
            # 生成受击音效
            hit_data = np.array([int(32767 * math.sin(2 * math.pi * 220 * i / 44100)) for i in range(44100 // 10)], dtype=np.int16)
            hit_stereo = np.column_stack((hit_data, hit_data))  # 转换为立体声音频
            hit_sound = pygame.sndarray.make_sound(hit_stereo)
            self.sounds['hit'] = hit_sound
            
            # 生成Boss死亡音效
            boss_death_data = np.array([int(32767 * math.sin(2 * math.pi * 110 * i / 44100)) for i in range(44100 // 2)], dtype=np.int16)
            boss_death_stereo = np.column_stack((boss_death_data, boss_death_data))  # 转换为立体声音频
            boss_death_sound = pygame.sndarray.make_sound(boss_death_stereo)
            self.sounds['boss_death'] = boss_death_sound
            
            # 生成金币音效
            coin_data = np.array([int(32767 * math.sin(2 * math.pi * 1760 * i / 44100)) for i in range(44100 // 20)], dtype=np.int16)
            coin_stereo = np.column_stack((coin_data, coin_data))  # 转换为立体声音频
            coin_sound = pygame.sndarray.make_sound(coin_stereo)
            self.sounds['coin'] = coin_sound
            
            print("音效生成成功:", list(self.sounds.keys()))
        except Exception as e:
            print("音效生成失败:", e)
            pass
        
        # 开始游戏
        self.start_game()
    
    def start_game(self):
        # 初始化玩家
        self.player = Player(100, SCREEN_HEIGHT - 100)
        
        # 加载关卡
        self.level = Level(self.current_level)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == GAME_STATE['playing']:
                        self.current_state = GAME_STATE['paused']
                    elif self.current_state == GAME_STATE['paused']:
                        self.current_state = GAME_STATE['playing']
                elif event.key == pygame.K_SPACE:
                    if self.current_state == GAME_STATE['menu']:
                        self.current_state = GAME_STATE['playing']
                    elif self.current_state == GAME_STATE['playing']:
                        self.player.jump()
                        if 'jump' in self.sounds:
                            self.sounds['jump'].play()
                    elif self.current_state == GAME_STATE['game_over'] or self.current_state == GAME_STATE['victory']:
                        self.start_game()
                        self.current_state = GAME_STATE['playing']
                elif event.key == pygame.K_f:
                    if self.current_state == GAME_STATE['playing']:
                        self.player.attack(self.bullets)
                        if 'attack' in self.sounds:
                            self.sounds['attack'].play()
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.player.move(0)
        
        # 持续按键处理
        keys = pygame.key.get_pressed()
        if self.current_state == GAME_STATE['playing']:
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            elif keys[pygame.K_RIGHT]:
                self.player.move(1)
        
        return True
    
    def update(self):
        if self.current_state == GAME_STATE['playing']:
            # 更新玩家
            self.player.update(self.level.platforms)
            
            # 更新关卡
            attack_result = self.level.update(self.player)
            
            # 处理Boss攻击返回的子弹
            if attack_result:
                # 检查返回的是否是子弹
                from bullet import Bullet
                from enemy import Enemy
                if isinstance(attack_result, Bullet):
                    self.bullets.add(attack_result)
                    print("Boss发射了子弹")
                elif isinstance(attack_result, Enemy):
                    print("Boss召唤了敌人")
                else:
                    print("Boss的攻击结果:", type(attack_result))
            
            # 更新子弹
            for bullet in self.bullets:
                bullet.update()
            
            # 碰撞检测
            self.check_collisions()
            
            # 检查游戏状态
            self.check_game_state()
    
    def check_collisions(self):
        # 子弹与敌人碰撞
        for bullet in self.bullets:
            enemy_hits = pygame.sprite.spritecollide(bullet, self.level.enemies, False)
            for enemy in enemy_hits:
                enemy.take_damage(1)
                bullet.kill()
            
            # 子弹与Boss碰撞
            if self.level.boss:
                if pygame.sprite.collide_rect(bullet, self.level.boss):
                    if not hasattr(self.level.boss, 'shielded') or not self.level.boss.shielded:
                        self.level.boss.take_damage(1)
                    bullet.kill()
        
        # 玩家与敌人碰撞
        damaged = False
        enemy_hits = pygame.sprite.spritecollide(self.player, self.level.enemies, False)
        if enemy_hits and not damaged and not self.player.invincible:
            self.player.health -= 1
            if 'hit' in self.sounds:
                self.sounds['hit'].play()
            self.player.invincible = True
            self.player.invincible_timer = pygame.time.get_ticks()
            damaged = True
            if self.player.health <= 0:
                self.current_state = GAME_STATE['game_over']
        
        # 玩家与Boss碰撞
        if self.level.boss and not damaged and not self.player.invincible:
            if pygame.sprite.collide_rect(self.player, self.level.boss):
                self.player.health -= 1
                if 'hit' in self.sounds:
                    self.sounds['hit'].play()
                self.player.invincible = True
                self.player.invincible_timer = pygame.time.get_ticks()
                damaged = True
                if self.player.health <= 0:
                    self.current_state = GAME_STATE['game_over']
        
        # 玩家与道具碰撞
        item_hits = pygame.sprite.spritecollide(self.player, self.level.items, True)
        for item in item_hits:
            if isinstance(item, Coin):
                self.score += item.value
                if 'coin' in self.sounds:
                    self.sounds['coin'].play()
            elif isinstance(item, Heart):
                self.player.health = min(self.player.health + item.value, 10)
    
    def check_game_state(self):
        # 检查是否通关
        if self.level.boss and hasattr(self.level.boss, 'health') and self.level.boss.health <= 0:
            if 'boss_death' in self.sounds:
                self.sounds['boss_death'].play()
            if self.current_level == 2:
                self.current_state = GAME_STATE['victory']
            else:
                self.current_level += 1
                self.level = Level(self.current_level)
                self.player.rect.x = 100
                self.player.rect.y = SCREEN_HEIGHT - 100
    
    def draw(self):
        if self.current_state == GAME_STATE['playing'] or self.current_state == GAME_STATE['paused']:
            # 绘制关卡
            self.level.draw(self.screen)
            
            # 绘制玩家
            self.player.draw(self.screen)
            
            # 绘制子弹
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            # 绘制UI
            self.draw_ui()
            
            # 绘制暂停界面
            if self.current_state == GAME_STATE['paused']:
                self.draw_pause_screen()
        elif self.current_state == GAME_STATE['menu']:
            self.draw_menu()
        elif self.current_state == GAME_STATE['game_over']:
            self.draw_game_over()
        elif self.current_state == GAME_STATE['victory']:
            self.draw_victory()
        
        # 更新屏幕
        pygame.display.flip()
    
    def draw_ui(self):
        # 绘制生命值
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # 绘制分数
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 50))
        
        # 绘制关卡
        level_text = font.render(f"Level: {self.current_level}", True, WHITE)
        self.screen.blit(level_text, (10, 90))
        
        # 绘制Boss血条
        if self.level.boss and hasattr(self.level.boss, 'health'):
            max_health = 8 if self.current_level == 1 else 12
            health_percent = self.level.boss.health / max_health
            pygame.draw.rect(self.screen, RED, (SCREEN_WIDTH // 2 - 100, 10, 200, 20))
            pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH // 2 - 100, 10, 200 * health_percent, 20))
            boss_health_text = font.render(f"Boss Health: {self.level.boss.health}/{max_health}", True, WHITE)
            self.screen.blit(boss_health_text, (SCREEN_WIDTH // 2 - boss_health_text.get_width() // 2, 15))
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        title_text = font.render("Super Platformer Adventure", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
        
        font = pygame.font.Font(None, 36)
        start_text = font.render("Press SPACE to start", True, WHITE)
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 400))
    
    def draw_pause_screen(self):
        font = pygame.font.Font(None, 72)
        pause_text = font.render("Paused", True, WHITE)
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 250))
        
        font = pygame.font.Font(None, 36)
        resume_text = font.render("Press ESC to resume", True, WHITE)
        self.screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 350))
    
    def draw_game_over(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, RED)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
    
    def draw_victory(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        victory_text = font.render("Victory!", True, GREEN)
        self.screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 200))
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
    
    def run(self):
        running = True
        while running:
            # 处理事件
            running = self.handle_events()
            
            # 更新游戏
            self.update()
            
            # 绘制游戏
            self.draw()
            
            # 控制帧率
            self.clock.tick(FPS)
        
        # 退出游戏
        pygame.quit()

# 启动游戏
if __name__ == "__main__":
    game = Game()
    game.run()