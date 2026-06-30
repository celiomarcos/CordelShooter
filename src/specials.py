#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Elementos especiais (easter egg de socorro).

ET de Varginha: aparece quando o heroi esta com pouca vida e cruza a
tela na horizontal, flutuando. Ao ser atingido pelos tiros do heroi,
some e deixa cair um LifeBonus (coracao), que ao ser coletado recupera
vida. Ambos herdam de Entity.
"""
import math

from src import settings
from src.entity import Entity


class ET(Entity):
    def __init__(self, position, vx):
        super().__init__(settings.ET, position)
        self.vx = vx
        self._y0 = position[1]
        self._t = 0.0

    def update(self, dt_scale=1.0):
        self._t += dt_scale
        self.rect.x += round(self.vx * dt_scale)
        self.rect.centery = int(self._y0 + math.sin(self._t / 16.0) * 10)
        # saiu da tela: desaparece
        if (self.vx > 0 and self.rect.left > settings.WIN_WIDTH) or \
           (self.vx < 0 and self.rect.right < 0):
            self.health = 0



class LifeBonus(Entity):
    """Coracao que cai lentamente; cura o heroi ao ser coletado."""

    def __init__(self, position):
        super().__init__(settings.LIFE, position)
        self._x0 = position[0]
        self._t = 0.0

    def update(self, dt_scale=1.0):
        self._t += dt_scale
        self.rect.y += round(self.speed * dt_scale)
        self.rect.centerx = int(self._x0 + math.sin(self._t / 12.0) * 14)
        if self.rect.top > settings.WIN_HEIGHT:
            self.health = 0

