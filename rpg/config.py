__author__ = 'jbert'

import pygame
import pygame.mixer
import utils, entity, controller, map

pygame.init()

# game settings
size = (1080, 720)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption('DEMO')
clock = pygame.time.Clock()

pygame.mixer.init()

# controller and map setup
cont = controller.Controller(screen)
rmap = map.Map(screen).load('map3')
bmap = map.Map(screen).load('map2')

# all enemies on the map
enemies = pygame.sprite.Group()
# im not sure, mr. krabs
allies  = pygame.sprite.Group()
# all players on the map
players = pygame.sprite.Group()
# all enemies the players are battling
opponents = pygame.sprite.Group()
# all barriers that the players can't go through
barriers = pygame.sprite.Group()

# a pressed key queue
pressed_keys = []