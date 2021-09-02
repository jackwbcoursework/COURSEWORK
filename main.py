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

def draw_player_hunger(surf, x, y, pct):
    if pct < 0: 
        pct = 0 #if the percentage is a minus then it is locked at 0
    BAR_LENGTH = 100 #Bar length is established as a constant
    BAR_HEIGHT = 20 #Bar height is established as a constant
    fill = pct * BAR_LENGTH #the level of fill is determined by the percentage given mulitplied by the length of the bar
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) #the rectangle for the black outline is just the whole bar itself
    fill_rect = pg.Rect(x, y , fill, BAR_HEIGHT) #the rectangle for the actual filled space is determined by the level it is filled
    if pct > 0.6: # sets colour to green if hhunger is full
        col = GREEN 
    elif pct > 0.3: #colour set to yellow if hungry
        col = YELLOW
    else:
        col = RED #red is added for when player is starving
    pg.draw.rect(surf, col, fill_rect) #rectangle is drawn
    pg.draw.rect(surf, BLACK, outline_rect, 2) #black outline given so it stands out.


    
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y) #drawn topleft
        if align == "ne":
            text_rect.topright = (x, y) #drawn topright
        if align == "sw":
            text_rect.bottomleft = (x, y) #drawn bottomleft
        if align == "se":
            text_rect.bottomright = (x, y) #drawn bottomright
        if align == "n":
            text_rect.midtop = (x, y) #drawn midtop
        if align == "s":
            text_rect.midbottom = (x, y) #drawn midbottom
        if align == "e":
            text_rect.midright = (x, y) #drawn midright
        if align == "w":
            text_rect.midleft = (x, y) #drawn midleft
        if align == "center":
            text_rect.center = (x, y) #drawn center
        self.screen.blit(text_surface, text_rect) #draws text to screen


    def load_data(self):
        game_folder = path.dirname(__file__) #identifies game folder
        img_folder = path.join(game_folder, "img") #defines image folder
        map_folder = path.join(game_folder, "map") #defines map folder
        snd_folder = path.join(game_folder, "snd") #defines sound folder
        amb_folder = path.join(game_folder, "ambience") #defines folder for ambient noises
        self.font = path.join(img_folder, "text.ttf") #loads font
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
        self.item_images = {} #multiple item images so needs to be stored in a dictionary
        for item in ITEM_IMAGES: #for every item in the item images dictionary...
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
            #that images item is loaded
        #SOUND LOADING
        pg.mixer.music.load(path.join(amb_folder, BG_AMBIENCE))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        self.weapon_sounds["spray"] = []
        for snd in WEAPON_SOUNDS:
            self.weapon_sounds["spray"].append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.mob_sounds = {}
        for type in BEAR_SOUNDS:
            self.mob_sounds[type] = pg.mixer.Sound(path.join(snd_folder, BEAR_SOUNDS[type]))
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates() #creates all sprite group
        self.walls = pg.sprite.Group() #creates a wall sprite group
        self.mobs = pg.sprite.Group() # creates a mob sprite group
        self.projectiles = pg.sprite.Group() # creates projectiles group
        self.items = pg.sprite.Group() #creates item group
        self.flare = pg.sprite.Group()
        #for row, tiles in enumerate(self.map.data): #gives both index and value for each row
        #    for col, tile in enumerate(tiles): # gives both index and value for each column
        #        if tile == '1':
        #            Wall(self, col, row) #spawns a wall if 1 is present
        #        if tile == 'P':
        #            self.player = Player(self, col, row) #spawns a player if P is present
        #        if tile == 'M':
        #            Bear(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                Bear(self, obj_center.x, obj_center.y)
            if tile_object.name in ["flare"]:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ["health"]:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ["food"]:
                Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height) #spawns camera
        self.draw_debug = False
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True #playing set to true
        pg.mixer.music.play(loops=-1)
        while self.playing: #MAIN GAME LOOP
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update() #updates all sprites
        self.camera.update(self.player) #updates camera to focus on player
        self.player.starve(HUNGER_LOSS) #constant hunger is updated
        #player picks up item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "flare": # if the item type is a flair
                hit.kill() #sprite is deleted
                self.effects_sounds["fgun"].play()
                if len(self.flare) == 0:
                    self.playing = False
            if hit.type == "health" and self.player.health < PLAYER_HEALTH: #if the item is a health pickup
                hit.kill() # item is picked up
                self.effects_sounds["health"].play()
                self.player.add_health(HEALTH_PACK_AMOUNT) #the add health method is called
            if hit.type == "food" and self.player.hunger < PLAYER_HUNGER: #if a food item is picked up and hunger is below max
                hit.kill() #remove the apple
                self.effects_sounds["apple"].play()
                self.player.add_hunger(APPLE_REPLENISH) #hunger bar is replenished


        #mob collision with player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect) #establish a basic sprite collide between groups
        for hit in hits: #for every hit
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
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
            draw_player_hunger(self.screen , 10, 30, self.player.hunger / PLAYER_HUNGER)
            self.draw_text("Remaining flare parts: {}".format(len(self.flare)), self.font, 30, WHITE, WIDTH - 10, 10, align="ne")
            if self.paused:
                self.draw_text("Paused", self.font, 105, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
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
                if event.key == pg.K_p:
                    self.paused = not self.paused

#Menus

    def show_start_screen(self):
        self.screen.fill(DARKGREEN) #fills screen
        self.draw_text("Welcome to Forest Survivor", self.font, 50, BLACK, WIDTH / 2, HEIGHT * 1 / 4, align = "center") #displays text
        self.draw_text("Press I for instructions", self.font, 50, BLACK, WIDTH / 2, HEIGHT * 2/ 4 , align = "center") #displays text
        self.draw_text("Press ENTER to start game", self.font, 50, BLACK, WIDTH / 2, HEIGHT * 3 / 4, align = "center") #displays text
        pg.display.flip() #shows the screen
        self.wait_for_key_menu() #waits for keys - menu version

    def show_go_screen(self): 
        if len(self.flare) == 0: #if all flares have been collected
            self.screen.fill(BLACK) #screen goes black
            self.draw_text("Congratulations, you have survived.", self.font, 50, WHITE, WIDTH / 2, HEIGHT / 2, align = "center") #white font displays
            self.draw_text("Press any key to return to start", self.font, 50, RED, WIDTH / 2, HEIGHT * 3 / 4 , align = "center" ) #more text
            pg.display.flip() #display made visible
            self.wait_for_key() #waits for key input
        else: #any other time game is ended
            self.screen.fill(BLACK) #black screen again
            self.draw_text("You are dead.", self.font, 75, RED, WIDTH / 2, HEIGHT / 2, align = "center") #death is indicated
            self.draw_text("Press any key to return to start", self.font, 50, RED, WIDTH / 2, HEIGHT * 3 / 4 , align = "center" ) #option to return to start
            pg.display.flip() #display flipped
            self.wait_for_key() #waits for key input

    def instructions(self):
        self.screen.fill(BLACK) #black screen filled
        self.draw_text("Collect all flare parts to call for rescue and escape.", self.font, 35, WHITE, WIDTH / 2, HEIGHT * 2 / 8, align = "center") #text
        self.draw_text("Avoid the bears and manage your hunger bar along the way.", self.font, 35, WHITE, WIDTH / 2, HEIGHT * 4 / 8, align = "center") #text
        self.draw_text("Space bar can be used to defend yourself, and P will pause the game.", self.font, 30, WHITE, WIDTH / 2, HEIGHT * 5 / 8, align = "center") #text
        self.draw_text("Press ENTER to start the game", self.font, 35, WHITE, WIDTH / 2, HEIGHT * 7 / 8, align = "center") #text
        pg.display.flip() #display flipped to make menu visible
        self.wait_for_key_menu() #wait for key - menu version


    def wait_for_key(self):
        pg.event.wait() #waits for an event
        waiting = True  #waiting variable
        while waiting: #while waiting
            self.clock.tick(FPS) #clock keeps ticking
            for event in pg.event.get(): #for each event
                if event.type == pg.QUIT: #if game is quit
                    waiting = False #no longer waiting
                    self.quit() #quit function is run
                if event.type == pg.KEYUP: #if any key is pressed
                    waiting = False #game restarts

    def wait_for_key_menu(self):
        pg.event.wait() #waits for event
        standby = True #standing by
        while standby: #while standing by
            self.clock.tick(FPS) #clock ticks
            for event in pg.event.get(): #for each event
                if event.type == pg.KEYDOWN: # if the event is a key press
                    if event.key == pg.K_RETURN: #if key is pressed
                        standby = False #standby is false and game continues
                    if event.key == pg.K_i: # if I is pressed
                        standby = False #standby is false
                        self.instructions() # instructions function is called
                if event.type == pg.QUIT: #if event type is to quit
                    standby = False #standby is false
                    self.quit() #game is quit

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
