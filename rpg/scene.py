__author__ = 'jbert'

import pygame
import sound
from config import (
    screen,
    cont,
    pressed_keys,
    rmap,
    players,
    enemies
)

from popup import Dialog, Attack

class Scene(object):
    def __init__(self, screen, rmap, players, enemies):
        self.screen = screen
        self.rmap = rmap
        self.players = players
        self.enemies = enemies
        self.entities = pygame.sprite.Group()
        self.entities.add(players)
        self.entities.add(enemies)
        self.pressed_keys = []

    def render(self):
        self.rmap.draw()
        self.entities.draw(self.screen)

    def update(self):
        for e in self.entities:
            e.refresh()
        pygame.display.flip()

    def handle_events(self, event_poll):
        for event in event_poll:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.append(event.key)
                for player in self.players:
                    cont.press(event.key, player)
            elif event.type == pygame.KEYUP:
                try:
                    self.pressed_keys.remove(event.key)
                except:
                    pass
                if not self.pressed_keys:
                    for player in self.players:
                        player.stop()
                else:
                    for player in self.players:
                        cont.press(self.pressed_keys[0], player)

    def close_scene(self):
        self.pressed_keys = []


class GeneralScene(Scene):
    def __init__(self, screen, rmap, players, enemies):
        super(GeneralScene, self).__init__(screen, rmap, players, enemies)
        sound.SoundMixer('soundtracks/house.wav')

class MainScene(Scene):
    def __init__(self, screen, rmap, players, enemies):
        super(MainScene, self).__init__(screen, rmap, players, enemies)
        sound.SoundMixer('soundtracks/Wintry_Town_Loop.wav')

class BattleScene(Scene):
    def __init__(self, screen, rmap, players, enemies):
        super(BattleScene, self).__init__(screen, rmap, players, enemies)
        sound.SoundMixer('soundtracks/battle.wav')
    def handle_events(self, event_poll):
        for event in event_poll:
            if event.type == pygame.QUIT:
                exit()

    def commense_battle(self):
        self.render()
        self.update()
        pygame.display.flip()
        bd = Dialog(self.screen)
        bd.say('battle has begun')
        bd.wait_for_continue()
        while self.enemies and self.players:
            self.render()
            self.update()
            for entity in self.entities:
                print entity.hp
                if entity.hp == 0:
                    if entity in self.players:
                        self.players.remove(entity)
                    else:
                        self.enemies.remove(entity)

                if entity in self.players:
                    bd.say('fight?')
                    bd.wait_for_continue()
                    fight_menu = Attack(self.screen, entity)
                    fight_menu.wait_for_continue()
                    try:
                        fight_menu.carry_out('hit', [x for x in self.entities if x in self.enemies][0])
                    except:
                        '''
                        player attacked after enemy died. Happens when event.get()
                        returns multiple true values for key presses
                        '''
                        pass
        for p in self.players:
            p.stop()
            p.controls_active = True


#current_scene = MainScene(screen, rmap,
#                          players, enemies)