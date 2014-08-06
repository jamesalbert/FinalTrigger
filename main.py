import pygame

from rpg import (
    entity,
    utils,
    scene,
    collision,
    popup
)

from rpg.config import (
    size,
    screen,
    clock,
    cont,
    rmap,
    bmap,
    enemies,
    opponents,
    allies,
    players,
    barriers,
    pressed_keys
)

mainchar = entity.Player('sprites/player_sprite.png', 48, 64, screen)
mainchar.walk('south')

enemy = entity.Enemy('sprites/green_sprite.png', 48, 64, screen)
enemy.walk('east')
enemy.transform(200, 200)

#allies.add(mainchar)
players.add(mainchar)
enemies.add(enemy)
collisions = collision.CollisionHandler()


'''
 get x, y, width, and height of all bounds defined
 in tiled and create collision boxes out of them
'''
objects = rmap.tmx.objects
for o in objects:
    if o.visible:
        barrier = collision.Barrier(screen, o.x, o.y , o.width, o.height)
        barriers.add(barrier)


collisions.add_system(mainchar, barriers,
                      mainchar.stop, single=False)
current_scene = scene.MainScene(screen, rmap,
                                players, enemies)


def player_enemy_collision(mainchar, opponent):
    #global players
    global current_scene
    mainchar.ready_for_battle()
    opponent.ready_for_battle()
    opponents.add(opponent)
    enemies.remove(opponent)
    current_scene.close_scene()
    current_scene = scene.BattleScene(screen, bmap,
                                      players, opponents)
    current_scene.commense_battle()
    mainchar.return_from_battle()
    current_scene = scene.MainScene(screen, rmap,
                                    players, enemies)
    current_scene.pressed_keys = []


collisions.add_system(mainchar, enemies, player_enemy_collision)
def main():
    global current_scene
    while True:
        '''
         render, update, and handle events within the current scene
        '''
        current_scene.render()
        current_scene.update()
        current_scene.handle_events(pygame.event.get())
        collisions.detect_collisions()
        #update and fps
        pygame.display.flip()
        clock.tick(60)

main()