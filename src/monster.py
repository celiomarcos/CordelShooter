#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Monstros do folclore (Saci, Mula-sem-cabeca, Boitata).

Descem pela tela com um leve balanco horizontal (senoide) e atiram
para baixo de tempos em tempos. Herdam de Entity.
"""
import math
import random

from src import settings
from src.bullet import MonsterBullet
from src.entity import Entity


class Monster(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.cooldown = random.randint(20, settings.SHOOT_COOLDOWN[name])
        self._phase = random.uniform(0, math.tau)
        self._sway = random.randint(1, 3)
        self._start_x = position[0]
        self._t = 0

    def update(self):
        self._t += 1
        self.rect.y += self.speed
        self.rect.centerx = int(self._start_x + math.sin(self._t / 18.0 + self._phase) * self._sway * 6)
        if self.rect.top > settings.WIN_HEIGHT:
            self.health = 0
        if self.cooldown > 0:
            self.cooldown -= 1

    def try_shoot(self):
        """Atira para baixo quando a cadencia zera."""
        if self.cooldown == 0:
            self.cooldown = settings.SHOOT_COOLDOWN[self.name]
            return MonsterBullet((self.rect.centerx, self.rect.bottom))
        return None
