__author__ = 'jbert'

from fontutils import wrapline
import pygame
import session

class Popup(object):
    def __init__(self, screen):
        self.keys = {}
        keys = [k for k in dir(pygame) if 'K_' in k]
        for k in keys:
            self.keys[k.split('_')[1]] = getattr(pygame, k)
        self.screen = screen
        self.coords = {'x': 200, 'y': 200}
        self.font = pygame.font.Font('fonts/data-latin.ttf', 20)
        self.image = pygame.image.load('images/popup_menu.png').convert()
        self.rect = self.image.get_rect()
    def say(self, text=''):
        #self.wrapped = wrapline(text, self.font, 19)
        self.screen.blit(self.image, [self.coords['x'], self.coords['y']])
        self.render = self.font.render(text, True, [0, 0, 0])
        self.text_coords = [self.coords['x'] + 10, self.coords['y']]
        self.refresh()
        return self
    def refresh(self):
        self.screen.blit(self.render, self.text_coords)
        return self
    def clear(self):
        self.says()
        return self
    def continue_popup(self):
        pygame.event.get()
        key = pygame.key.get_pressed()
        return key[self.keys['SPACE']]
    def wait_for_continue(self):
        while not self.continue_popup():
            pygame.display.flip()
        while self.continue_popup():
            pygame.display.flip()
        return self


class Attack(Popup):
    def __init__(self, screen, player):
        super(Attack, self).__init__(screen)
        self.attack = player.attack
        choices = str()
        for a in self.attack:
            choices += '%s' % a
        self.say(choices)
    def carry_out(self, choice, player):
        chosen_attack = self.attack[choice]
        player.hp -= chosen_attack['power']
        return self


class Pause(Popup):
    def __init__(self, screen):
        super(Pause, self).__init__(screen)
        pass


class Dialog(Popup):
    '''
     Dialog class that renders a dialog box with specified text.

     These should be used for 'yes'-only popups
     example:
        sign = Dialog(screen)
        sign.say('this is a sign')
    '''
    def __init__(self, screen):
        super(Dialog, self).__init__(screen)
        self.okay = pygame.Surface([50, 50])
        self.okay.set_alpha(0)
        self.okay.fill([255,255,255])
        self.okay_rect = self.okay.get_rect()
        self.okay_rect.x = self.coords['x'] + 150 # 150 = image.width / 2
        self.okay_rect.y = self.coords['y'] + 75  # 75  = image.height / 2
        #print self.okay_rect.x, self.okay_rect.y
        self.okay_text = self.font.render('ok', True, [0, 0, 0])
        screen.blit(self.okay_text, [self.okay_rect.x,
                                     self.okay_rect.y])
        screen.blit(self.okay, [self.okay_rect.x,
                                self.okay_rect.y])