__author__ = 'jbert'

import pygame
import popup

class Controller:
    '''
     Controller class that handles key presses
    '''
    def __init__(self, screen):
        self.screen = screen
        self.keys = {}
        keys = [k for k in dir(pygame) if 'K_' in k]
        for k in keys:
            self.keys[k.split('_')[1]] = getattr(pygame, k)

    def press(self, key, player):
        if not player.controls_active:
            return
        player.stop()
        #print self.pressed_keys
        if key == self.keys['w']:
            player.speed['y'] = -2
            player.walk('north')
        elif key == self.keys['s']:
            player.speed['y'] = 2
            player.walk('south')
        elif key == self.keys['a']:
            player.speed['x'] = -2
            player.walk('west')
        elif key == self.keys['d']:
            player.speed['x'] = 2
            player.walk('east')