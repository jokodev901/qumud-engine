from __future__ import annotations
import uuid

from operator import itemgetter


class Entity:
    def __init__(self, name: str,
                 attackrate: int,
                 damage: int,
                 health: int,
                 range: int,
                 speed: int,
                 stance: str,
                 initiative: int = 1,
                 max_targets: int = 1) -> None:
        self.id = str(uuid.uuid4())
        self.isplayer = False
        self.name = name
        self.attackrate = attackrate
        self.damage = damage
        self.health = health
        self.range = range
        self.speed = speed
        self.max_targets = max_targets
        self.initiative = initiative
        self.position = None
        self.last_attack = None
        self.targets = []
        self.event = None
        self.stance = stance

    def attack(self, entity: Entity) -> int | None:
        entity.suffer(self.damage)
        return self.damage

    def move(self, distance) -> int | None:
        if self.event:
            self.position = (self.position + distance) % self.event.size
            return self.position

        return None

    def suffer(self, val: int) -> int:
        self.health -= val
        return self.health

    def add_targets(self, entity: Entity) -> None:
        self.targets.append(entity)

    def shortest_distance(self, pos) -> tuple[int, str]:
        inner_distance = abs(self.position - pos)
        outer_distance = (self.event.size - max(self.position, pos)) + min(self.position, pos)

        if inner_distance > outer_distance:
            return outer_distance, 'outer'

        return inner_distance, 'inner'

    def update_targets(self, prio_key: str, reverse: bool, sticky: bool) -> list | None:
        """
        Pick a primary target based on prio_key criteria, add additional targets by distance

        prio_key: entity key value to prioritize
        reverse: whether to prioritize prio_key value by reverse order (descending)
        sticky: optionally adds a uuid-based secondary sort to ensure initial target is maintained, only works for
                fixed values like range, initiative, speed
        """

        if self.event:
            elist = []
            etype = self.event.enemies if self.isplayer else self.event.players

            for e in etype:
                tdis, tdir = self.shortest_distance(e.position)
                elist.append({'target': e, 'range': e.range, 'distance': tdis, 'direction': tdir, 'id': e.id})

            if sticky:
                elist = sorted(elist, key=itemgetter('id'))

            targets = sorted(elist, key=itemgetter(prio_key), reverse=reverse)[:1]
            remainder = sorted(elist, key=itemgetter(prio_key), reverse=reverse)[1:]

            if self.max_targets > 1:
                secondary_targets = sorted(remainder, key=itemgetter('distance'))[:self.max_targets - 1]
                targets += secondary_targets

            self.targets = targets

            return self.targets

        return None