import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

#HUD
def draw_player_health(surf, x, y, pct):
    if pct < 0: 
        pct = 0 #if the percentage is a minus then it is locked at 0
    BAR_LENGTH = 100 #Bar length is established as a constant
    BAR_HEIGHT = 20 #Bar height is established as a constant
    fill = pct * BAR_LENGTH #the level of fill is determined by the percentage given mulitplied by the length of the bar
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) #the rectangle for the black outline is just the whole bar itself
    fill_rect = pg.Rect(x, y , fill, BAR_HEIGHT) #the rectangle for the actual filled space is determined by the level it is filled
    if pct > 0.6: # sets colour to green if health is relatively full
        col = GREEN 
    elif pct > 0.3: #colour set to yellow if moderate damage
        col = YELLOW
    else:
        col = RED #red is added for when player is in dire need of health
    pg.draw.rect(surf, col, fill_rect) #rectangle is drawn
    pg.draw.rect(surf, BLACK, outline_rect, 2) #black outline given so it stands out.

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__) #identifies game folder
        img_folder = path.join(game_folder, "img") #defines image folder
        map_folder = path.join(game_folder, "map") #defines map folder
        self.map = TiledMap(path.join(map_folder, 'map.tmx')) #loads map
        self.map_img = self.map.make_map() #map img defined
        self.map_rect = self.map_img.get_rect() #mao rect defined
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha() #loads player image
        self.player_imgr = pg.image.load(path.join(img_folder, PLAYER_IMG_R)).convert_alpha() #loads player image facing right
        self.player_imgl = pg.image.load(path.join(img_folder, PLAYER_IMG_L)).convert_alpha() #loads player image facing left
        self.player_imgw = pg.image.load(path.join(img_folder, PLAYER_IMG_U)).convert_alpha() #loads player image facing up
        self.player_imgd = pg.image.load(path.join(img_folder, PLAYER_IMG_D)).convert_alpha() #loads player image facing down
        self.spray_img = pg.image.load(path.join(img_folder, SPRAY_IMG)).convert_alpha() #loads bear spray sprite 
        self.bear_img = pg.image.load(path.join(img_folder, BEAR_IMG)).convert_alpha() #loads bear sprite
        
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group() #creates all sprite group
        self.walls = pg.sprite.Group() #creates a wall sprite group
        self.mobs = pg.sprite.Group() # creates a mob sprite group
        self.projectiles = pg.sprite.Group() # creates projectiles group
        #for row, tiles in enumerate(self.map.data): #gives both index and value for each row
        #    for col, tile in enumerate(tiles): # gives both index and value for each column
        #        if tile == '1':
        #            Wall(self, col, row) #spawns a wall if 1 is present
        #        if tile == 'P':
        #            self.player = Player(self, col, row) #spawns a player if P is present
        #        if tile == 'M':
        #            Bear(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                Bear(self, tile_object.x, tile_object.y)
        self.camera = Camera(self.map.width, self.map.height) #spawns camera
        self.draw_debug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True #playing set to true
        while self.playing: #MAIN GAME LOOP
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update() #updates all sprites
        self.camera.update(self.player) #updates camera to focus on player
        #mob collision with player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect) #establish a basic sprite collide between groups
        for hit in hits: #for every hit
            self.player.health -= BEAR_DAMAGE #the player health will be equal to itself minus the damage done
            hit.vel = vec(0, 0) #velocity set to 0
            if self.player.health <= 0: #if health is 0 or less
                self.playing = False #playing is set to false for reset
        if hits: #if a hit is recorded
            self.player.pos += vec(BEAR_KNOCKBACK, 0).rotate(-hits[0].rot) #the player is pushed back in the direction that the mob is facing

        #spray collision
        hits = pg.sprite.groupcollide(self.mobs, self.projectiles, False, True) #checks for collisions betweem groups)
        for hit in hits: #for every hit
            hit.health -= SPRAY_DMG #health is reduced by the correct damage
            hit.vel = vec(0,0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE): 
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT)) #draws lines along x axis
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y)) #draws line along y axis

    def draw(self):
        #self.screen.fill(BGCOLOR) #fills screen with background colour from constant
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect)) #draws camera
        #self.draw_grid()
        for sprite in self.all_sprites: #referencing every sprite in the game
            if isinstance(sprite, Bear): #if the sprite is an instance of the bear class
                sprite.draw_health() #then the health bar is drawn accordingly
            self.screen.blit(sprite.image, self.camera.apply(sprite)) #all sprites are drawn onto the screen
            if self.draw_debug:
                pg.draw.rect(self.screen, BLACK, self.camera.apply_rect(sprite.hit_rect), 1)
            if self.draw_debug:
                for wall in self.walls:
                    pg.draw.rect(self.screen, BLACK, self.camera.apply_rect(wall.rect), 1)

            #HUD drawn
            draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip() # display is flipped - crucial for consistent image

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
