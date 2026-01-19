import time
import random
import os
import copy

from entity import Entity
from event import Event


if __name__ == '__main__':
    """
    Test combat loop by creating an Event, spawning entities for each side, and updating until complete    
    """

    os.system('cls' if os.name == 'nt' else 'clear')
    event = Event(size=100, debug=False)
    teamsize = 100

    classes = [
        Entity(name='Pikeman', attackrate=1, damage=1, health=15, range=2, speed=1, max_targets=2, initiative=5),
        Entity(name='Berserker', attackrate=1, damage=5, health=10, range=1, speed=5, initiative=20),
        Entity(name='Archer', attackrate=1, damage=1, health=5, range=4, speed=2),
        Entity(name='Swordman', attackrate=1, damage=1, health=20, range=1, speed=2, initiative=10),
        Entity(name='Mage', attackrate=1, damage=1, health=5, range=3, speed=2, max_targets=3),
    ]

    playerlist = []
    enemylist = []

    for _ in range(teamsize):
        x = copy.deepcopy(classes[random.randint(0, len(classes) - 1)])
        event.add_player(x)

    for _ in range(teamsize):
        x = copy.deepcopy(classes[random.randint(0, len(classes) - 1)])
        event.add_enemy(x)

    while True:
        bfs = []
        populated_bfs = []
        for _ in range(min(teamsize, 50)):
            bfs.append([' '] * event.size)

        for player in event.players:
            for battlefield in bfs:
                if battlefield[player.position] == ' ':
                    if player.name == 'PikemanP':
                        battlefield[player.position] = 'P'
                    if player.name == 'BerserkerP':
                        battlefield[player.position] = 'B'
                    if player.name == 'ArcherP':
                        battlefield[player.position] = 'A'
                    if player.name == 'SwordmanP':
                        battlefield[player.position] = 'S'
                    if player.name == 'MageP':
                        battlefield[player.position] = 'M'
                    break

        for enemy in event.enemies:
            for battlefield in bfs:
                if battlefield[enemy.position] == ' ':
                    if enemy.name == 'Pikeman':
                        battlefield[enemy.position] = 'p'
                    if enemy.name == 'Berserker':
                        battlefield[enemy.position] = 'b'
                    if enemy.name == 'Archer':
                        battlefield[enemy.position] = 'a'
                    if enemy.name == 'Swordman':
                        battlefield[enemy.position] = 's'
                    if enemy.name == 'Mage':
                        battlefield[enemy.position] = 'm'
                    break

        for battlefield in bfs:
            print(''.join(battlefield))

        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

        if event.active:
            event.update()
        else:
            break
