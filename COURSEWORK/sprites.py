import pygame as pg
from settings import *
vec = pg.math.Vector2 #imports vector class

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites #adds player to the all sprites group
        pg.sprite.Sprite.__init__(self, self.groups) #initialises as sprite
        self.game = game #passes copy of game
        self.image = game.player_img
        self.rect = self.image.get_rect() #gives the sprite a rect
        self.vel = vec(0,0) #sets sprite velocity to 0 by default
        self.pos = vec(x, y) * TILESIZE #sets sprite position

    def get_keys(self):
        self.vel = vec(0, 0) #velocity set to 0
        keys = pg.key.get_pressed() #allows key inputs
        if keys[pg.K_LEFT] or keys[pg.K_a]: #if "a" key is pressed
            self.vel.x = -PLAYER_SPEED #go to the left on the x axis
            self.image = self.game.player_imgl
        if keys[pg.K_RIGHT] or keys[pg.K_d]: #if the "d" key is pressed
            self.vel.x = PLAYER_SPEED #go to the right on x axis
            self.image = self.game.player_imgr
        if keys[pg.K_UP] or keys[pg.K_w]: #if "w" key is pressed
            self.vel.y = -PLAYER_SPEED #go up on the y axis
            self.image = self.game.player_imgw
        if keys[pg.K_DOWN] or keys[pg.K_s]: #if "s" key is pressed 
            self.vel.y = PLAYER_SPEED #go down on the y axis
            self.image = self.game.player_imgd
        if self.vel.x != 0 and self.vel.y != 0: #allows diagonal movement 
            self.vel *= 0.7071 #allows the player to move diagonally
    

    def collide_with_walls(self, dir): #collide with walls function
        if dir == 'x': #if in the x direction
            hits = pg.sprite.spritecollide(self, self.game.walls, False) #sees if the player has hit a wall, will return true or false
            if hits: #if true
                if self.vel.x > 0: #if the x velocity is greater than 0
                    self.pos.x = hits[0].rect.left - self.rect.width #the player will be placed on the left of the rectangle, because they were heading right
                if self.vel.x < 0: #if the x velocity is less than 0
                    self.pos.x = hits[0].rect.right #the player will be placed on the right of the rectangle, as they were heading left
                self.vel.x = 0 #player movement stops
                self.rect.x = self.pos.x #sets player rectangle to new player position
        if dir == 'y': #if direction = y
            hits = pg.sprite.spritecollide(self, self.game.walls, False) #sees if the player has hit a wall, will return true or false
            if hits: #if true
                if self.vel.y > 0: #if the y velocity is greater than 0
                    self.pos.y = hits[0].rect.top - self.rect.height # the player is placed on top of the object, as they were moving down
                if self.vel.y < 0:#if the y velocity is less than 0
                    self.pos.y = hits[0].rect.bottom # the player is placed on the bottom of the object, as they were moving up
                self.vel.y = 0 # stops y velocity
                self.rect.y = self.pos.y #new rectangle to new position

    def update(self):
        self.get_keys() #gets key presses from get keys function
        self.pos += self.vel * self.game.dt #adds velocity to player position
        self.rect.x = self.pos.x #sets player rectangle to new position on x axis
        self.collide_with_walls('x') #checks for wall collisions on the x axis
        self.rect.y = self.pos.y #sets player rectangle to new position on y axis
        self.collide_with_walls('y') #checks for collisions on y axis

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y): #creates wall class with parameters of locations
        self.groups = game.all_sprites, game.walls #adds to wall class
        pg.sprite.Sprite.__init__(self, self.groups) #adds  to all sprite group and initalises it as a sprite
        self.game = game #passes copy of game
        self.image = pg.Surface((TILESIZE, TILESIZE)) #creates sprite as size of tile
        self.image.fill(GREEN) #fills wall in as green
        self.rect = self.image.get_rect() #gives rectangle to sprite
        self.x = x #sets position
        self.y = y #sets positiom
        self.rect.x = x * TILESIZE #sets rectangle position
        self.rect.y = y * TILESIZE #sets rectangle position
