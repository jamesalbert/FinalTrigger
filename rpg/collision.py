__author__ = 'jbert'

from config import mainchar, barriers, screen, players
import pygame
import scene

class CollisionHandler:
    def __init__(self):
        '''
         self.pairs = [[sprite, sprite, callback]]
        '''
        self.systems = []
    def detect_collisions(self):
        for system in self.systems:
            player, trigger, callback, args, single = system
            if isinstance(trigger, pygame.sprite.Group):
                #print player
                #print trigger
                #print dir(trigger)
                #print len(trigger)
                collided_with = pygame.sprite.spritecollide(player,
                                                            trigger,
                                                            single)
                if collided_with:
                    callback(player, collided_with.pop())
            elif isinstance(trigger, pygame.sprite.Sprite):
                if pygame.sprite.collide_rect(player, trigger):
                    callback(*args)
            #if collided_with:
                #print len(trigger)
                #for e in trigger:
                #    print e
                #pygame.time.wait(10000)
                #print system
                #print isinstance(system[1], pygame.sprite.Group)
        return self
    def add_system(self, player, trigger, callback, args=[], single=True):
        self.systems.append((player, trigger, callback, args, single))
        return self
    def clear_systems(self):
        self.systems = []
    def refresh(self):
        self.screen.blit(self.image, [self.rect.x,
                                      self.rect.y])


class Threshold(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, callback):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.Surface([width, height])
        self.image.set_alpha(255)
        self.image.fill([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.map = str()
        self.callback = None


def coords_to_barrier(e, callback, props=None):
    global collhand
    if hasattr(e, 'x'):
        if mainchar.coords['x'] == e.x \
            and mainchar.coords['y'] == e.y:
            return
        box = Barrier(screen, e.x, e.y , e.width, e.height)
        if props:
            # doors
            new_scene = scene.MainScene
            if e.parent.properties.get('env') == 'outside':
                new_scene = scene.GeneralScene
            print e
            print new_scene
            box.map = props.get('map')
            #print props
            args = [box.map, players, pygame.sprite.Group(), new_scene]
            collhand.add_system(mainchar, box, callback, args=args, single=True)
        else:
            # walls
            barriers.add(box)


collhand = CollisionHandler()
collhand.add_system(mainchar, barriers,
                    mainchar.stop, single=False)