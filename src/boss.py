#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Chefe da fase: a Cuca.

Entra pelo topo, desce ate uma faixa fixa e passa a se mover na
horizontal. Alterna entre tres padroes de ataque, ficando bem mais
ameacadora que os monstros comuns. Derrota-la e a condicao de vitoria.

Padroes (em ciclo):
  0 - rajada tripla MIRADA no heroi;
  1 - cortina em LEQUE (7 chamas) cobrindo a tela;
  2 - dois jatos retos saindo das laterais do focinho.
"""
import math

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
        self._pattern = 0

    # ------------------------------------------------------------------
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

    # --- auxiliares de tiro -------------------------------------------
    def _origin(self):
        return (self.rect.centerx, self.rect.bottom)

    def _fan(self, deg):
        ang = math.radians(deg)
        sp = settings.SPEED[settings.BOSS_BULLET]
        return BossBullet(self._origin(), (math.sin(ang) * sp, math.cos(ang) * sp))

    def _aimed(self, target, jitter_deg=0.0):
        sx, sy = self._origin()
        ang = math.atan2(target.rect.centery - sy, target.rect.centerx - sx)
        ang += math.radians(jitter_deg)
        sp = settings.SPEED[settings.BOSS_BULLET]
        return BossBullet((sx, sy), (math.cos(ang) * sp, math.sin(ang) * sp))

    # ------------------------------------------------------------------
    def try_shoot(self, target):
        if self._entering or self.cooldown != 0:
            return []
        self.cooldown = settings.SHOOT_COOLDOWN[self.name]
        self._pattern = (self._pattern + 1) % 3

        if self._pattern == 0:
            return [self._aimed(target, j) for j in (-12, 0, 12)]
        if self._pattern == 1:
            return [self._fan(d) for d in (-45, -30, -15, 0, 15, 30, 45)]
        return [
            BossBullet((self.rect.centerx - 22, self.rect.bottom)),
            BossBullet((self.rect.centerx + 22, self.rect.bottom)),
        ]
