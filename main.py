import time
import random
import os
import copy
import math

from entity import Entity
from event import Event
from generators import generate_npcs, generate_monsters

from itertools import zip_longest


def big_random_battle():
    os.system('cls' if os.name == 'nt' else 'clear')
    event = Event(size=100, debug=False)
    teamsize = 50

    classes = [
        Entity(name='Pikeman', attackrate=1, damage=1, health=15, range=2, speed=1, max_targets=2, stance='skirmish',
               initiative=5),
        Entity(name='Berserker', attackrate=1, damage=5, health=10, range=1, speed=4, stance='skirmish', initiative=10),
        Entity(name='Archer', attackrate=1, damage=1, health=5, range=4, speed=3, stance='skirmish'),
        Entity(name='Swordman', attackrate=1, damage=2, health=20, range=1, speed=2, stance='skirmish', initiative=5),
        Entity(name='Mage', attackrate=1, damage=1, health=5, range=3, speed=2, stance='skirmish', max_targets=3),
        Entity(name='Cavalry', attackrate=1, damage=3, health=15, range=2, speed=8, stance='assassin', max_targets=2),
    ]

    for _ in range(teamsize):
        x = copy.deepcopy(classes[random.randint(0, len(classes) - 1)])
        event.add_player(x)

    for _ in range(teamsize):
        x = copy.deepcopy(classes[random.randint(0, len(classes) - 1)])
        event.add_enemy(x)

    while True:
        bfs = []
        for _ in range(min(teamsize, 50)):
            bfs.append([' '] * event.size)

        for player in event.players:
            for battlefield in bfs:
                if battlefield[player.position] == ' ':
                    if player.name == 'PikemanP':
                        battlefield[player.position] = '⟶'
                    if player.name == 'BerserkerP':
                        battlefield[player.position] = '🪓'
                    if player.name == 'ArcherP':
                        battlefield[player.position] = '🏹'
                    if player.name == 'SwordmanP':
                        battlefield[player.position] = '🤺'
                    if player.name == 'MageP':
                        battlefield[player.position] = '🧙'
                    if player.name == 'CavalryP':
                        battlefield[player.position] = '🏇'
                    break

        for enemy in event.enemies:
            for battlefield in bfs:
                if battlefield[enemy.position] == ' ':
                    if enemy.name == 'Pikeman':
                        battlefield[enemy.position] = '⟵'
                    if enemy.name == 'Berserker':
                        battlefield[enemy.position] = '🪓'
                    if enemy.name == 'Archer':
                        battlefield[enemy.position] = '🏹'
                    if enemy.name == 'Swordman':
                        battlefield[enemy.position] = '🤺'
                    if enemy.name == 'Mage':
                        battlefield[enemy.position] = '🧛'
                    if enemy.name == 'Cavalry':
                        battlefield[enemy.position] = '🏇'
                    break

        i = len(bfs) - 1
        while i >= 0:
            if i % 2 == 0:
                print(''.join(bfs[i]))
            i -= 1

        i = 0
        while i < len(bfs):
            if i % 2 == 1:
                print(''.join(bfs[i]))
            i += 1

        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

        if event.active:
            event.update()
        else:
            break


def procgen_battle():
    os.system('cls' if os.name == 'nt' else 'clear')
    event = Event(size=100, debug=False)
    teamsize = 10
    level = 50

    seed = input(f'''Input a seed value
    >''')

    for npc in generate_npcs(count=teamsize, seed=seed, level=level):
        event.add_player(npc)

    for monster in generate_monsters(count=teamsize, seed=seed, level=level):
        event.add_enemy(monster)

    event.update_status_log()
    event.update_combat_log()
    looptime = time.time()

    while True:
        bfs = []
        combat_logs = event.read_combat_log(min_time=looptime)
        event_status = event.read_status_log(min_time=looptime)

        for status, combat in zip(event_status, combat_logs):
            for _ in range(min(teamsize, 50)):
                bfs.append([' '] * event.size)

            status_bars = []
            for player, enemy in zip_longest(status['players'], status['enemies']):
                playerlen = 0
                enemylen = 0
                playerstats = ''
                enemystats = ''

                if player:
                    playerstats = (f" [{''.join(['='] * math.ceil((player['health'] / player['max_health']) * 10))
                                       + ''.join([' '] * (10 - math.ceil((player['health'] / player['max_health'])
                                                                         * 10)))}]"
                                   f" {player['name']} D{player['damage']} S{player['speed']} R{player['range']}")
                    playerlen = len(playerstats)

                if enemy:
                    enemystats = (f"{enemy['name']}"
                                 f" D{enemy['damage']}"
                                 f" S{enemy['speed']}"
                                 f" R{enemy['range']}"
                                 f" [{''.join(['='] * math.ceil((enemy['health'] / enemy['max_health']) * 10))
                                      + ''.join([' '] * (10 - math.ceil((enemy['health'] / enemy['max_health'])
                                                                        * 10)))}] ")
                    enemylen = len(enemystats)

                padding = event.size - (playerlen + enemylen)
                status_bars.append(f'{playerstats}{''.join([' '] * padding)}{enemystats}')

                for battlefield in bfs:
                    if player:
                        if battlefield[player['position']] == ' ':
                            battlefield[player['position']] = player['name'][0]
                            break

                for battlefield in bfs:
                    if enemy:
                        if battlefield[enemy['position']] == ' ':
                            battlefield[enemy['position']] = enemy['name'][0].lower()
                            break

            i = len(bfs) - 1
            while i >= 0:
                if i % 2 == 0:
                    print(''.join(bfs[i]))
                i -= 1

            i = 0
            while i < len(bfs):
                if i % 2 == 1:
                    print(''.join(bfs[i]))
                i += 1

            for bar in status_bars:
                print(bar)

            for log in combat['logs']:
                print(log['msg'])

            looptime = time.time()
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')

        if event.active:
            event.update()
        else:
            break


if __name__ == '__main__':
    x = input('''
        Choose a demo:
        1 - Big Random Battle
        2 - Procgen NPC vs Monster Battle w/seed
    >''')

    if x == '1':
        big_random_battle()
    elif x == '2':
        procgen_battle()