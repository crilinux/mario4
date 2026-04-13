# 游戏常量定义

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# 玩家设置
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = -20
GRAVITY = 1

# 敌人设置
ENEMY_SPEED = 2

# 子弹设置
BULLET_SPEED = 8

# 关卡设置
TILE_SIZE = 32

# 游戏状态
GAME_STATE = {
    'menu': 0,
    'playing': 1,
    'paused': 2,
    'game_over': 3,
    'victory': 4
}