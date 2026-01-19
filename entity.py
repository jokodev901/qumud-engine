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

    def update_targets(self) -> list | None:
        """
        If entity is in an event, update list of targets by vicinity
        """
        if self.event:
            elist = []
            etype = self.event.enemies if self.isplayer else self.event.players

            for e in etype:
                tdis, tdir = self.shortest_distance(e.position)
                elist.append({'target': e, 'distance': tdis, 'direction': tdir})

            self.targets = sorted(elist, key=itemgetter('distance'))[:self.max_targets]
            return self.targets

        return None