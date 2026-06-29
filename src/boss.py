#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Chefe da fase: a Cuca.

Entra pelo topo, desce ate uma faixa fixa e passa a se mover na
horizontal, disparando rajadas de BossBullet. Derrota-la e a condicao
de vitoria do jogo.
"""
from src import settings
from src.bullet import BossBullet
from src.entity import Entity


class Boss(Entity):
    def __init__(self, position):
        super().__init__(settings.BOSS, position)
        self.cooldown = settings.SHOOT_COOLDOWN[self.name]
        self._direction = 1
        self._target_y = 90
        self._entering = True

    def update(self):
        if self._entering:
            self.rect.y += self.speed
            if self.rect.top >= self._target_y:
                self._entering = False
        else:
            self.rect.x += self.speed * self._direction
            if self.rect.right >= settings.WIN_WIDTH or self.rect.left <= 0:
                self._direction *= -1
        if self.cooldown > 0:
            self.cooldown -= 1

    def try_shoot(self):
        """Dispara dois projeteis (esquerda/direita do focinho)."""
        if self._entering or self.cooldown != 0:
            return []
        self.cooldown = settings.SHOOT_COOLDOWN[self.name]
        return [
            BossBullet((self.rect.centerx - 18, self.rect.bottom)),
            BossBullet((self.rect.centerx + 18, self.rect.bottom)),
        ]
