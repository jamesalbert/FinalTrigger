__author__ = 'jbert'

import pygame

class SoundMixer(object):
    def __init__(self, soundfile):
        pygame.mixer.fadeout(1000)
        self.sound = pygame.mixer.Sound(soundfile)
        print 2
        self.sound.play()