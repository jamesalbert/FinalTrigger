__author__ = 'jbert'

import pygame

class SoundMixer(object):
    def __init__(self, soundfile):
        pygame.mixer.stop()
        self.sound = pygame.mixer.Sound(soundfile)
        self.sound.play()