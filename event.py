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
        self.combat_log_buffer = []
        self.combat_log = []
        self.status_log = []
        self.debug_log_buffer = []
        self.active = True

    def end(self) -> None:
        self.active = False

    def add_player(self, player: Entity) -> None:
        player.position = (int((self.size / 2) - random.randrange(10,20))) + player.initiative
        player.name += 'P'
        if self.debug:
            print(f'adding player {player.name} at position {player.position}')
        player.event = self
        player.isplayer = True
        self.players.append(player)

    def add_enemy(self, enemy: Entity) -> None:
        enemy.position = (int((self.size / 2) + random.randrange(10, 20))) - enemy.initiative
        if self.debug:
            print(f'adding enemy {enemy.name} at position {enemy.position}')
        enemy.event = self
        self.enemies.append(enemy)

    def move_entity(self, entity: Entity) -> None:
        entity.position = (entity.position + entity.speed) % self.size
        
    def update_combat_log(self):
        if not self.combat_log_buffer:
            timestamp = 0
            buffer = []
        else:
            timestamp = time.time()
            buffer = self.combat_log_buffer

        self.combat_log.append({'time': timestamp, 'logs': buffer})
        self.clear_combat_log_buffer()

    def write_combat_log(self, msg: str) -> None:
        if self.debug:
            print(msg)
        self.combat_log_buffer.append({'time': time.time(), 'msg': msg})

    def read_combat_log(self, min_time: float = None, max_time: float = None) -> list:
        buffer = self.combat_log

        if min_time:
            buffer = [log for log in buffer if log['time'] >= min_time]
        if max_time:
            buffer = [log for log in buffer if log['time'] <= max_time]

        return buffer

    def clear_combat_log_buffer(self) -> None:
        self.combat_log_buffer = []
        
    def update_status_log(self) -> None:
        if not self.status_log:
            timestamp = 0
        else:
            timestamp = time.time()

        plist = []
        elist = []


        for player in self.players:
            plist.append({k: v for k, v in player.__dict__.items() if not k.startswith('__')})

        for enemy in self.enemies:
            elist.append({k: v for k, v in enemy.__dict__.items() if not k.startswith('__')})

        status = {'time': timestamp, 'players': plist, 'enemies': elist}
        self.status_log.append(status)

    def read_status_log(self, min_time: float = None, max_time: float = None) -> list:
        buffer = self.status_log

        if min_time:
            buffer = [status for status in buffer if status['time'] >= min_time]

        if max_time:
            buffer = [status for status in buffer if status['time'] <= max_time]

        return buffer

    def clear_status_log(self) -> None:
        self.status_log = []
        
    def write_debug_log(self, msg: str) -> None:
        if self.debug:
            print(msg)
        self.debug_log_buffer.append(msg)

    def read_debug_log(self) -> list:
        return self.debug_log_buffer

    def clear_debug_log(self) -> None:
        self.debug_log_buffer = []

    def action_assassin(self, entity: Entity) -> None:
        """
        Entity will prioritize target with the greatest range, and will not switch targets until dead

        """

        targets = entity.update_targets(prio_key='range', reverse=True, sticky=True)

        if self.debug:
            print(f'{entity.name} is at position {entity.position} before processing actions')

        move_buffer = []
        attack_buffer = []
        will_move = False

        for target in targets:
            # if we flag will_move then no reason to continue evaluating other targets
            if will_move:
                break

            if self.debug:
                print(f'{entity.name} looping targets: {target['target'].name}, {target['distance']},'
                      f' {target['target'].position}')

            not_in_atk_range = entity.range < target['distance']

            if not_in_atk_range:
                will_move = True
                dir = 1 if entity.position < target['target'].position else -1

                # Flip direction if outer
                if target['direction'] != 'inner':
                    dir *= -1

                distance = (min(entity.speed, (abs(target['distance'] - entity.range)))) * dir
                move_buffer.append((entity, distance))

                if self.debug:
                    print(f'{entity.name} move {distance} with range {entity.range} based on:'
                          f'target: {target['target'].name} distance: {target["distance"]} range: {target['target'].range}'
                          f' not_in_atk_range: {not_in_atk_range}')

            else:
                if target['distance'] <= entity.range:
                    attack_buffer.append((entity, target['target']))

        if will_move:
            self.move_buffer += move_buffer
        else:
            self.attack_buffer += attack_buffer



    def action_skirmish(self, entity: Entity) -> None:
        """
        Entity will prioritize targeting the closest targets, opting to "back up" and out-range when viable

        Define skirmish-specific actions here
        """

        targets = entity.update_targets(prio_key='distance', reverse=False, sticky=False)

        if self.debug:
            print(f'{entity.name} is at position {entity.position} before processing actions')

        move_buffer = []
        attack_buffer = []
        will_move = False

        for target in targets:
            # if we flag will_move then no reason to continue evaluating other targets
            if will_move:
                break

            if self.debug:
                print(f'{entity.name} looping targets: {target['target'].name}, {target['distance']},'
                      f' {target['target'].position}')

            not_in_atk_range = entity.range < target['distance']
            worth_kiting = math.ceil(((min(entity.range, entity.speed) - target['target'].range)
                                      / max(target['target'].speed, 1))) >= 2
            in_enemy_range = target['target'].range >= target['distance']

            if not_in_atk_range or (worth_kiting and in_enemy_range):
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

    def process_actions(self, entity: Entity) -> None:
        if entity.stance == 'skirmish':
            self.action_skirmish(entity)

        elif entity.stance == 'assassin':
            self.action_assassin(entity)


    def update(self) -> None:
        if self.active:
            tickrate = 1
            ticks = math.floor((time.time() - self.last_updated) / tickrate)

            if self.debug:
                ticks = 1

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
                            self.write_combat_log(msg)
                            print(msg)
                            self.end()
                            return

                    for enemy in self.enemies:
                        if self.players:
                            self.process_actions(entity=enemy)
                        else:
                            msg = "All players are dead"
                            self.write_combat_log(msg)
                            print(msg)
                            self.end()
                            return

                    # apply buffered attack actions
                    if self.attack_buffer:
                        for attack in self.attack_buffer:
                            logmsg = f'{attack[0].name} hits {attack[1].name} for {attack[0].damage} damage'
                            self.write_combat_log(logmsg)
                            attack[0].attack(entity=attack[1])

                    # evaluate enemy health
                    for enemy in self.enemies:
                        if enemy.health <= 0:
                            self.write_combat_log(f'{enemy.name} is dead')
                            self.enemies.remove(enemy)

                    # evaluate players health
                    for idx, player in enumerate(self.players):
                        if player.health <= 0:
                            self.write_combat_log(f'{player.name} is dead')
                            del self.players[idx]

                    # apply buffered move actions
                    if self.move_buffer:
                        for move in self.move_buffer:
                            if move[0] not in self.players and move[0] not in self.enemies:
                                continue
                            self.write_combat_log(f'{move[0].name} moves {move[1]}')
                            move[0].move(distance=move[1])

                    self.update_status_log()
                    self.update_combat_log()
                    self.attack_buffer = []
                    self.move_buffer = []

                self.last_updated = time.time()
