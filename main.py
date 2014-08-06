import pygame

from rpg.collision import coords_to_barrier, collhand
#from rpg.scene import current_scene
from rpg import (
    entity,
    utils,
    scene,
    collision,
    popup,
    map
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
    pressed_keys,
    mainchar,
    enemy,
    doors
)


def change_scene(mapname, players, enemies, new_scene=scene.GeneralScene):
    global current_scene
    doors.empty()
    barriers.empty()
    collhand.clear_systems()
    rmap = map.Map(screen, mapname)
    current_scene = new_scene(screen, rmap,
                              players, enemies)
    find_bounds()
    print barriers
    collhand.add_system(mainchar, barriers,
                        mainchar.stop, single=False)
    collhand.add_system(mainchar, enemies, player_enemy_collision)
    #current_scene.pressed_keys = []

def find_bounds():
    global current_scene
    print 'now in %s' % str(current_scene)
    for e in current_scene.rmap.tmx:
        obj_name = e.properties.get('obj_name')
        #print dir(e)
        #print e.properties
        print e.name
        if e.name == 'brown_house_door':
            for e_child in e:
                coords_to_barrier(e_child, change_scene, props=e.properties)
        elif e.name == 'spawn':
            #print e.properties
            for spawn in e:
                mainchar.transform(spawn.x, spawn.y)
        elif e.name == 'exit':
            #print e.properties
            for ex in e:
                coords_to_barrier(ex, change_scene, props=e.properties)
        else:
            coords_to_barrier(e, change_scene)


def player_enemy_collision(mainchar, opponent):
    #global players
    global current_scene
    mainchar.ready_for_battle()
    opponent.ready_for_battle()
    opponents.add(opponent)
    enemies.remove(opponent)
    change_scene('map2', players, opponents, new_scene=scene.BattleScene)
    #current_scene = scene.BattleScene(screen, bmap,
    #                                  players, opponents)
    current_scene.commense_battle()
    mainchar.return_from_battle()
    change_scene('map3', players, enemies, new_scene=scene.MainScene)
    #current_scene = scene.MainScene(screen, rmap,
    #                                players, enemies)
    #current_scene.pressed_keys = []


#collhand.add_system(mainchar, enemies, player_enemy_collision)

def main():
    global current_scene
    change_scene('map3', players, enemies, scene.MainScene)
#    find_bounds()
    while True:
        '''
         render, update, and handle events within the current scene
        '''
        current_scene.render()
        current_scene.update()
        current_scene.handle_events(pygame.event.get())
        collhand.detect_collisions()
        #update and fps
        pygame.display.flip()
        clock.tick(60)

main()