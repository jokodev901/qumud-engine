import time
import io
import random
import math

from entity import Entity


class Event:
    def __init__(self, size: int, debug: bool = False):
        # in DB, entities would FK to Event, here we will process a list
        # other things here would be hazards/biome modifiers
        self.size = size
        self.players = []
        self.enemies = []
        self.attack_buffer = []
        self.move_buffer = []
        self.last_updated = time.time()
        self.debug = debug
        self.combat_log_buffer = io.StringIO()
        self.debug_log_buffer = io.StringIO()
        self.active = True

    def end(self) -> None:
        self.active = False
        combat_log_output = self.combat_log_buffer.getvalue()
        self.combat_log_buffer.close()
        self.debug_log_buffer.close()

        file_path = "combat_log.txt"
        with open(file_path, "w") as f:
            f.write(combat_log_output)

    def add_player(self, player: Entity) -> None:
        player.position = (int((self.size / 2) - random.randrange(5,15))) + player.initiative
        player.name += 'P'
        if self.debug:
            print(f'adding player {player.name} at position {player.position}')
        player.event = self
        player.isplayer = True
        self.players.append(player)

    def add_enemy(self, enemy: Entity) -> None:
        enemy.position = (int((self.size / 2) + random.randrange(5, 15))) - enemy.initiative
        if self.debug:
            print(f'adding enemy {enemy.name} at position {enemy.position}')
        enemy.event = self
        self.enemies.append(enemy)

    def move_entity(self, entity: Entity) -> None:
        entity.position = (entity.position + entity.speed) % self.size

    def combat_log(self, msg: str) -> None:
        print(msg, file=self.combat_log_buffer)

    def debug_log(self, msg: str) -> None:
        print(msg, file=self.debug_log_buffer)

    def process_actions(self, entity: Entity) -> None:
        # Targeting (opportunistic)
        targets = entity.update_targets()
        if self.debug:
            print(f'{entity.name} is at position {entity.position} before processing actions')

        move_buffer = []
        attack_buffer = []
        will_move = False
        i = 0

        for target in targets:
            i += 1 # only evaluate moving based on nearest target

            if self.debug:
                print(f'{entity.name} looping targets: {target['target'].name}, {target['distance']},'
                      f' {target['target'].position}')

            not_in_atk_range = entity.range < target['distance']
            worth_kiting = math.ceil(((min(entity.range, entity.speed) - target['target'].range)
                                      / max(target['target'].speed, 1))) >= 2
            in_enemy_range = target['target'].range >= target['distance']

            if (not_in_atk_range or (worth_kiting and in_enemy_range)) and i == 1:
                will_move = True
                dir = 1 if entity.position < target['target'].position else -1

                # Move away if too close
                if target['distance'] < entity.range:
                    dir *= -1

                # Flip direction if outer
                if target['direction'] != 'inner':
                    dir *= -1

                # Random direction if same position
                if entity.position == target['target'].position:
                    dir *= random.randint(-1, 1)

                distance = (min(entity.speed, (abs(target['distance'] - entity.range)))) * dir
                move_buffer.append((entity, distance))

                if self.debug:
                    print(f'{entity.name} move {distance} with range {entity.range} based on:'
                          f'target: {target['target'].name} distance: {target["distance"]} range: {target['target'].range}'
                          f' not_in_atk_range: {not_in_atk_range},'
                          f' or worth_kiting: {worth_kiting},'
                          f' and in_enemy_range: {in_enemy_range}')

            else:
                if target['distance'] <= entity.range:
                    attack_buffer.append((entity, target['target']))

        if will_move:
            self.move_buffer += move_buffer
        else:
            self.attack_buffer += attack_buffer


    def update(self):
        if self.active:
            tickrate = 1
            ticks = math.floor((time.time() - self.last_updated) / tickrate)

            if ticks >= tickrate:
                if self.debug:
                    print(f'{ticks} ticks for this update')

                for _ in range(ticks):
                    # process actions for players and enemies
                    for player in self.players:
                        if self.enemies:
                            self.process_actions(entity=player)
                        else:
                            msg = "All enemies are dead"
                            self.combat_log(msg)
                            print(msg)
                            self.end()
                            return

                    for enemy in self.enemies:
                        if self.players:
                            self.process_actions(entity=enemy)
                        else:
                            msg = "All players are dead"
                            self.combat_log(msg)
                            print(msg)
                            self.end()
                            return

                    # apply buffered attack actions
                    if self.attack_buffer:
                        for attack in self.attack_buffer:
                            logmsg = f'{attack[0].name} hits {attack[1].name} for {attack[0].damage} damage'
                            self.combat_log(logmsg)
                            attack[0].attack(entity=attack[1])

                    # evaluate enemy health
                    for enemy in self.enemies:
                        if enemy.health <= 0:
                            self.combat_log(f'{enemy.name} is dead')
                            self.enemies.remove(enemy)
                        else:
                            self.combat_log(f'{enemy.name} health {enemy.health}')

                    # evaluate players health
                    for idx, player in enumerate(self.players):
                        if player.health <= 0:
                            self.combat_log(f'{player.name} is dead')
                            del self.players[idx]
                        else:
                            self.combat_log(f'{player.name} health: {player.health}')

                    # apply buffered move actions
                    if self.move_buffer:
                        for move in self.move_buffer:
                            if move[0] not in self.players and move[0] not in self.enemies:
                                continue
                            self.combat_log(f'{move[0].name} moves {move[1]}')
                            move[0].move(distance=move[1])

                    self.attack_buffer = []
                    self.move_buffer = []

                self.last_updated = time.time()