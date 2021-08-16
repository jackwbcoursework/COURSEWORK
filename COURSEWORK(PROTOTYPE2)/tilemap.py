import pygame as pg
from settings import *
import pytmx



#class Map:
    #def __init__(self, filename):
        #self.data = [] #creates empty data list
        #with open(filename, 'rt') as f: #opens file to read
            #for line in f: #for every line in file
                #self.data.append(line.strip()) #add the data into the empty data list

        #self.tilewidth = len(self.data[0]) #width of map is the first line of list
        #self.tileheight = len(self.data) #height of map is the number of lines
        #self.width = self.tilewidth * TILESIZE #pixel width
        #self.height = self.tileheight * TILESIZE #pixel height

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True) #uses pytmx to load file, pixelalpha keeps transparency
        self.width = tm.width * tm.tilewidth #width of the map multiplied by the width of pixels in each tile
        self.height = tm.height * tm.tileheight #height of the map multiplied by the height of pixels in each tile
        self.tmxdata = tm #stored in data variable

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid #gets tile ID - ti is the shortened version of command
        for layer in self.tmxdata.visible_layers: #for every layer set as visible
            if isinstance(layer, pytmx.TiledTileLayer): #of it's an instance of the tile layer
                for x, y, gid, in layer: #get the x y and gid
                    tile = ti(gid) #run the previous id command
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight)) #blit the title onto the screen

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height)) #creates a temporary surface
        self.render(temp_surface) #calls render command
        return temp_surface #returns result


class Camera: 
    def __init__(self, width, height): #gives camera a width and height
        self.camera = pg.Rect(0, 0, width, height) #gives camera a rectangle to track offset
        self.width = width #size of whole map
        self.height = height #size of whole map

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft) # return rectangle location of entity and move it by camera coordinates
        #move command when applied to a rect = gives a new rectangle shifted by specified amount
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
        #offset can now be applied to rectangle

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2) #moves offset in opposite direction of player along x axis
        y = -target.rect.y + int(HEIGHT / 2) #moves offset in opposite direction of player along y axis

        # limit scrolling to map size
        x = min(0, x)  # x is the minimum of what 0 or x are: if x = 1 then the minimum is still 0
        y = min(0, y)  # (see above example)
        x = max(-(self.width - WIDTH), x)  # right side
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height) #moves camera to next location with same dimensions
