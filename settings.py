import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 100, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "CourseworkProject"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 30, 30)
PLAYER_SPEED = 200
PLAYER_HUNGER = 200

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
DETECT_RADIUS = 400
BEAR_IMG = "tile001.png"

#Weapon settings
SPRAY_IMG = "sprayblu.png"
SPRAY_SPEED = 500
SPRAY_RANGE = 500
SPRAY_RATE = 500
SPRAY_DMG = 50

#Item properties
ITEM_IMAGES = {"flare": "FGun.png", "health": "medkit.png", "food": "apple.png"} #dictionary so multiple items can be referenced
HEALTH_PACK_AMOUNT = 50
APPLE_REPLENISH = 50
HUNGER_LOSS = 0.03
HUNGER_RATE = 1

#Item animation settings
BOB_RANGE = 15
BOB_SPEED = 0.5



#Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
PROJ_LAYER = 3
MOB_LAYER = 2
#EFFECTS_LAYER = 4


#Sounds
BG_AMBIENCE = "forest.wav"
PLAYER_HIT_SOUNDS = ["pain1.wav", "pain2.wav", "pain3.wav"]
BEAR_SOUNDS = {"bear": "bear2.wav"}
EFFECTS_SOUNDS = {"health": "health.wav", "fgun": "fgun.wav" , "apple": "apple.wav"}
WEAPON_SOUNDS = ["spray.wav"]
