import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        self.data = [] #creates empty data list
        with open(filename, 'rt') as f: #opens file to read
            for line in f: #for every line in file
                self.data.append(line.strip()) #add the data into the empty data list

        self.tilewidth = len(self.data[0]) #width of map is the first line of list
        self.tileheight = len(self.data) #height of map is the number of lines
        self.width = self.tilewidth * TILESIZE #pixel width
        self.height = self.tileheight * TILESIZE #pixel height

class Camera: 
    def __init__(self, width, height): #gives camera a width and height
        self.camera = pg.Rect(0, 0, width, height) #gives camera a rectangle to track offset
        self.width = width #size of whole map
        self.height = height #size of whole map

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft) # return rectangle location of entity and move it by camera coordinates
        #move command when applied to a rect = gives a new rectangle shifted by specified amount

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2) #moves offset in opposite direction of player along x axis
        y = -target.rect.y + int(HEIGHT / 2) #moves offset in opposite direction of player along y axis

        # limit scrolling to map size
        x = min(0, x)  # x is the minimum of what 0 or x are: if x = 1 then the minimum is still 0
        y = min(0, y)  # (see above example)
        x = max(-(self.width - WIDTH), x)  # right side
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height) #moves camera to next location with same dimensions
