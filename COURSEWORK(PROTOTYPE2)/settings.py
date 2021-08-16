import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 30, 30)
PLAYER_SPEED = 200
#Player images
PLAYER_IMG = "chard1.png"
PLAYER_IMG_R = "charr1.png"
PLAYER_IMG_L = "charl1.png"
PLAYER_IMG_D = "chard1.png"
PLAYER_IMG_U = "charw1.png"

#Mob settings
BEAR_SPEED = 100
BEAR_HEALTH = 100
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
BEAR_DAMAGE = 50
BEAR_KNOCKBACK =50
AVOID_RADIUS = 50
BEAR_IMG = "tile001.png"

#Weapon settings
SPRAY_IMG = "sprayblu.png"
SPRAY_SPEED = 500
SPRAY_RANGE = 500
SPRAY_RATE = 500
SPRAY_DMG = 50



