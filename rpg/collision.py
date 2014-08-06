__author__ = 'jbert'

import pygame

class CollisionHandler:
    def __init__(self):
        '''
         self.pairs = [[sprite, sprite, callback]]
        '''
        self.systems = []
    def detect_collisions(self):
        for system in self.systems:
            players, trigger, callback, single = system
            collided_with = pygame.sprite.spritecollide(players,
                                                        trigger,
                                                        single)
            if collided_with:
                callback(players, collided_with.pop())
        return self
    def add_system(self, players, trigger, callback, single=True):
        self.systems.append((players, trigger, callback, single))
        return self


class Barrier(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.Surface([width, height])
        self.image.set_alpha(255)
        self.image.fill([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def refresh(self):
        self.screen.blit(self.image, [self.rect.x,
                                      self.rect.y])