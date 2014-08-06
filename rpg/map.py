__author__ = 'jbert'

import pygame
import pytmx
import pyscroll

size = (1080, 720)


class Map:
    '''
     Map class that loads a .tmx file and renders it to the screen
     example:
        map = Map(screen).load('dungeon').draw()
    '''
    def __init__(self, screen):
        self.screen = screen
    def load(self, filename):
        self.tmx = pytmx.load_pygame('%s.tmx' % filename, pixelalpha=True)
        self.tmap = pyscroll.TiledMapData(self.tmx)
        self.map_layer = pyscroll.BufferedRenderer(self.tmap, size)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        return self
    def draw(self):
        self.group.center([0,0])
        self.group.draw(self.screen)
        return self