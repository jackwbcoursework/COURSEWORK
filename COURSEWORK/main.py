import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

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
        self.map = Map(path.join(game_folder, 'map.txt')) #loads map
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha() #loads player image
        self.player_imgr = pg.image.load(path.join(img_folder, PLAYER_IMG_R)).convert_alpha() #loads player image facing right
        self.player_imgl = pg.image.load(path.join(img_folder, PLAYER_IMG_L)).convert_alpha() #loads player image facing left
        self.player_imgw = pg.image.load(path.join(img_folder, PLAYER_IMG_U)).convert_alpha() #loads player image facing up
        self.player_imgd = pg.image.load(path.join(img_folder, PLAYER_IMG_D)).convert_alpha() #loads player image facing down

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group() #creates all sprite group
        self.walls = pg.sprite.Group() #creates a wall sprite group
        for row, tiles in enumerate(self.map.data): #gives both index and value for each row
            for col, tile in enumerate(tiles): # gives both index and value for each column
                if tile == '1':
                    Wall(self, col, row) #spawns a wall if 1 is present
                if tile == 'P':
                    self.player = Player(self, col, row) #spawns a player if P is present
        self.camera = Camera(self.map.width, self.map.height) #spawns camera

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

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE): 
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT)) #draws lines along x axis
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y)) #draws line along y axis

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

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
