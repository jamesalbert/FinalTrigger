__author__ = 'jbert'

from spritesheet import SpriteStripAnim
import pygame

compass = ('south', 'west', 'east', 'north')
foot_x_const = .25
foot_y_const = .85
foot_w_const = .50
foot_h_const = .25

class Sprite(pygame.sprite.Sprite):
    '''
     Base class for all sprites
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Entity(Sprite):
    '''
     Base class for all characters

     filename (string) - filename of spritesheet
     column (int) - get rid of this
     clip_width (int) - width of individual frame
     clip_height (int) - height of individual frame
     screen (pygame.Surface) - current screen (used for blitting)
    '''
    def __init__(self,
                 filename,
                 clip_width,
                 clip_height,
                 screen):
        Sprite.__init__(self)
        self.screen = screen
        self.directions = {}
        self.clip_width = clip_width
        self.clip_height = clip_height
        for direction, clip in zip(compass, range(4)):
            # tuples for sprites are:
            #   (start_x, start_y, clip_width, clip_height)
            self.directions[direction] = (0, clip_height*clip,
                                          clip_width,
                                          clip_height)
        self.filename = filename
        self.coords = {'x': 0, 'y': 0}
        self.speed = {'x': 0, 'y': 0}
        self.hp = 100
        self.image = pygame.Surface([clip_width*foot_w_const,
                                     clip_height*foot_h_const])
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.update_bounds()
        self.controls_active = True
    def update_bounds(self):
        '''
        self.rect.{x,y} are the coordinates of surface bounding
        the character. This surface is used for collisions
        and orientation.
        '''
        self.rect.x = self.coords['x'] + self.clip_width * foot_x_const
        self.rect.y = self.coords['y'] + self.clip_height * foot_y_const
        return self
    def walk(self, direction):
        '''
        direction (string) - direction to face (ie 'north')
        '''
        # filename, (x, y, w, h), count, colorkey, loop, frames
        self.strip = SpriteStripAnim(self.filename, \
                                     self.directions[direction], \
                                     3, (255,255,255), True, 10)
        self.strip.iter()
        return self
    def transform(self, x, y):
        '''
        put the character on (x,y) point on the x,y-plane
        '''
        self.coords['x'] = x
        self.coords['y'] = y
        return self
    def transport(self):
        '''
        move the character along the respective axis with
        respect to the current speed.
        '''
        self.coords['x'] += self.speed['x']
        self.coords['y'] += self.speed['y']
        return self
    def stop(self, *args):
        '''
        stop the character
        '''
        self.coords['x'] -= self.speed['x']
        self.coords['y'] -= self.speed['y']
        self.speed['x'] = 0
        self.speed['y'] = 0
        return self
    def refresh(self):
        '''
        self.transport() - update character's current position
        self.current_image... - update animation
        self.update_bounds() - self-explanatory
        self.screen.blit... - put character on screen
        '''
        self.transport()
        self.current_image = self.strip.next()
        self.update_bounds()
        self.screen.blit(self.current_image, (self.coords['x'], self.coords['y']))
        return self
    def ready_for_battle(self):
        '''
        custom callback for battles
        examples of use:
          - change position
          - change direction
          - turn off certain controls
        '''
        raise NotImplementedError


class Player(Entity):
    def __init__(self,
                 filename,
                 clip_width,
                 clip_height,
                 screen):
        super(Player, self).__init__(filename,
                                     clip_width,
                                     clip_height,
                                     screen)
        self.attack = {'hit': {'power': 20}}
    def ready_for_battle(self):
        self.transform(100, 300)
        self.walk('east')
        self.controls_active = False
        self.stop()
        return self
    def return_from_battle(self):
        self.controls_active = True
        self.coords = {'x': 0, 'y': 0}
        return self


class MainChar(Player):
    def __init__(self,
                 filename,
                 clip_width,
                 clip_height,
                 screen):
        super(MainChar, self).__init__(filename,
                                       clip_width,
                                       clip_height,
                                       screen)
        self.name = 'Ari'

class Enemy(Entity):
    def ready_for_battle(self):
        self.transform(500, 300)
        self.walk('west')
        self.stop()