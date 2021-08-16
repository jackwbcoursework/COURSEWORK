import pygame as pg
from settings import *
vec = pg.math.Vector2 #imports vector class

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites #adds player to the all sprites group
        pg.sprite.Sprite.__init__(self, self.groups) #initialises as sprite
        self.game = game #passes copy of game
        self.dir = dir
        self.image = game.player_img
        self.rect = self.image.get_rect() #gives the sprite a rect
        self.rect.x = x #defines position
        self.rect.y = y #defines position
        self.hit_rect = PLAYER_HIT_RECT # gives player hitbox
        self.hit_rect.center = self.rect.center #centers hitbox
        self.vel = vec(0,0) #sets sprite velocity to 0 by default
        self.pos = vec(x, y) #sets sprite position
        self.last_shot = 0
        self.health = PLAYER_HEALTH

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

        if keys[pg.K_SPACE]: #if the space bar is hit
            now = pg.time.get_ticks() #ticks are taken
            if now - self.last_shot > SPRAY_RATE:
                self.last_shot = now
                self.dir = self.vel
                Spray(self.game, self.pos, self.dir)

                
        if self.vel.x != 0 and self.vel.y != 0: #allows diagonal movement 
            self.vel *= 0.7071 #allows the player to move diagonally

    def update(self):
        self.get_keys() #gets key presses from get keys function
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt #adds velocity to player position
        self.hit_rect.centerx = self.pos.x #sets player rectangle to new position on x axis
        collide_with_walls(self, self.game.walls,'x') #checks for wall collisions on the x axis
        self.hit_rect.centery = self.pos.y #sets player rectangle to new position on y axis
        collide_with_walls(self, self.game.walls,'y') #checks for collisions on y axis

class Bear(pg.sprite.Sprite):
    def __init__(self, game, x, y): #creates bear class with parameters of locations
        self.groups = game.all_sprites, game.mobs #adds to relevant class
        pg.sprite.Sprite.__init__(self, self.groups) #adds  to all sprite group and initalises it as a sprite
        self.game = game # passes copy of the game so that the player can be referenced for the update function.
        self.image = game.bear_img # gives the bear its image
        self.image = pg.transform.scale(self.image,(TILESIZE, TILESIZE))
        self.rect = self.image.get_rect() # gives rectangle
        self.rect.x = x #defines position
        self.rect.y = y #defines position
        self.hit_rect = MOB_HIT_RECT.copy() #gives mob hit rect
        self.hit_rect.center = self.rect.center #centers hit rect
        self.pos = vec(x, y) # location of enemy
        self.vel = vec(0,0) #how fast the bear is moving at any time, default 0
        self.acc = vec(0,0) #to stop the mob from instantly turning to the player directed
        self.rot = 0 #gives a default rotation value
        self.rect.center = self.pos #centers position
        self.health = BEAR_HEALTH #enemy health


    def avoid_mobs(self):
        for mob in self.game.mobs: #for every mob
            if mob != self: #and for mobs that do not include the sprite itself
                dist = self.pos - mob.pos #calculate distance
                if 0 < dist.length() < AVOID_RADIUS: #if distance is greater than 0 and less than the constant
                    self.acc += dist.normalize() #acceleration is distance normalized (length of 1)


    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0)) # gives player direction
        self.image = pg.transform.rotate(self.game.bear_img, self.rot) #rotates sprite in that direction
        self.rect = self.image.get_rect() #gives image updated rectangle
        self.rect.center = self.pos # gives an updates centered rectangle at the given position
        self.acc = vec(1, 0).rotate(-self.rot) #calculates acceleration
        self.avoid_mobs() #calls avoid mobs
        self.acc.scale_to_length(BEAR_SPEED) #sets acceleration to be the speed at which has been set in settings, rotated in the direction that is required
        self.acc += self.vel * -1 #as the enemy goes faster, this value will increase which will control acceleration
        self.vel += self.acc * self.game.dt # velocity is added to acceleration and delta time
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2 # equation of motion - velocity multiplied by delta time add 0.5 * acceleration * delta time again squared by 2
        self.hit_rect.centerx = self.pos.x #updates centered sprite
        collide_with_walls(self, self.game.walls, "x") #mob collision on x axis
        self.hit_rect.centery = self.pos.y #updates centered sprite
        collide_with_walls(self, self.game.walls, "y") #mob collision on y axis
        self.rect.center = self.hit_rect.center #establishes rectangle center
        if self.health <= 0: #if enemy health goes equal to or below 0
            self.kill() #enemy is deleted

    def draw_health(self):
        if self.health > 60: #if the health of the bear is greater than 60
            col = GREEN # colour of bar is green
        elif self.health > 30: #if greater than 30
            col = YELLOW #colour is yellow
        else: #if neither of the above conditions are true
            col = RED # the colour is set to red

        width = int(self.rect.width * self.health / BEAR_HEALTH) #width of the bar is the rectangle width, multiplied by the percentage of health remaining
        self.health_bar = pg.Rect(0, 0, width, 7) #a rectangle is then added with these parameters
        if self.health < BEAR_HEALTH: #if health is below designated health
            pg.draw.rect(self.image, col, self.health_bar) #bar is drawn


class Spray(pg.sprite.Sprite):
    def __init__(self, game, pos, dir): #initiates sprite with a specified postition and direction
        self.groups = game.all_sprites, game.projectiles #assigned two groups for sprites
        pg.sprite.Sprite.__init__(self, self.groups) #initiated as a sprite
        self.game = game
        self.image = game.spray_img #image set to the one loaded in load data
        pg.transform.scale(self.image ,(TILESIZE, TILESIZE))
        self.rect = self.image.get_rect() #rectangle given
        self.hit_rect = self.rect
        self.pos = vec(pos) #position established
        self.rect.center = pos #center of rectangle added made equal to position of sprite
        self.vel = vec(dir) * SPRAY_SPEED #direction is just a vector of where the bullet should travel, for movement this needs to be multiplied by the speed
        self.spawn_time = pg.time.get_ticks() #when to delete the bullet tracked

    def update(self):
        self.pos += self.vel * self.game.dt # velocity added to position
        self.rect.center = self.pos #rectangle updated to that position
        if pg.time.get_ticks() - self.spawn_time > SPRAY_RANGE:
            self.kill()



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

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h): #creates wall class with parameters of locations
        self.groups = game.walls #adds to wall class
        pg.sprite.Sprite.__init__(self, self.groups) #adds  to all sprite group and initalises it as a sprite
        self.game = game #passes copy of game
        self.rect = pg.Rect( x, y, w, h) #creates rectangle
        self.x = x #sets position
        self.y = y #sets positiom
        self.rect.x = x  #sets rectangle position
        self.rect.y = y  #sets rectangle position