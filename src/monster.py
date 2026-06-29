#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Monstros do folclore, cada um com movimento e ataque proprios.

  - Saci-Perere : desce aos saltos e atira MIRANDO no heroi (com erro,
                  de tao travesso).
  - Mula-sem-cabeca : desce rapido em linha e solta um COICE DE FOGO,
                  uma rajada tripla descendente.
  - Boitata     : serpenteia devagar e cospe um LEQUE DE FOGO (5 chamas).

Todos herdam de Entity. try_shoot(target) devolve uma lista de tiros
(pode ser vazia), permitindo um ou varios projeteis por disparo.
"""
import math
import random

from src import settings
from src.bullet import MonsterBullet
from src.entity import Entity

# parametros de movimento por tipo: amplitude e frequencia do balanco
# horizontal e multiplicador da velocidade vertical.
_MOVE = {
    "saci": {"amp": 26, "freq": 9.0, "vy": 1.0},
    "mula": {"amp": 6, "freq": 16.0, "vy": 1.7},
    "boitata": {"amp": 44, "freq": 20.0, "vy": 0.8},
}


class Monster(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        base = settings.SHOOT_COOLDOWN[name]
        self.cooldown = random.randint(base // 2, base)
        self._phase = random.uniform(0, math.tau)
        self._start_x = position[0]
        self._t = 0
        self._mv = _MOVE.get(name, {"amp": 10, "freq": 18.0, "vy": 1.0})

    # ------------------------------------------------------------------
    def update(self):
        self._t += 1
        mv = self._mv
        vy = self.speed * mv["vy"]
        if self.name == "saci":  # desce aos saltos
            vy *= 0.5 + abs(math.sin(self._t / 8.0))
        self.rect.y += int(round(vy))
        offset = math.sin(self._t / mv["freq"] + self._phase) * mv["amp"]
        self.rect.centerx = int(self._start_x + offset)
        if self.rect.top > settings.WIN_HEIGHT:
            self.health = 0
        if self.cooldown > 0:
            self.cooldown -= 1

    # --- auxiliares de tiro -------------------------------------------
    def _origin(self):
        return (self.rect.centerx, self.rect.bottom)

    def _down(self):
        return MonsterBullet(self._origin())

    def _fan(self, deg):
        """Tiro inclinado 'deg' graus em relacao a vertical (para baixo)."""
        ang = math.radians(deg)
        sp = settings.SPEED[settings.MONSTER_BULLET]
        return MonsterBullet(self._origin(), (math.sin(ang) * sp, math.cos(ang) * sp))

    def _aimed(self, target, jitter_deg=0.0):
        sx, sy = self._origin()
        ang = math.atan2(target.rect.centery - sy, target.rect.centerx - sx)
        ang += math.radians(jitter_deg)
        sp = settings.SPEED[settings.MONSTER_BULLET]
        return MonsterBullet((sx, sy), (math.cos(ang) * sp, math.sin(ang) * sp))

    # ------------------------------------------------------------------
    def try_shoot(self, target):
        # so atira ja dentro da tela e enquanto estiver na parte de cima
        if self.rect.bottom < 10 or self.rect.centery > settings.WIN_HEIGHT * 0.7:
            return []
        if self.cooldown > 0:
            return []
        self.cooldown = settings.SHOOT_COOLDOWN[self.name] + random.randint(-8, 16)

        if self.name == "saci":
            return [self._aimed(target, random.uniform(-10, 10))]
        if self.name == "mula":
            return [self._fan(-18), self._down(), self._fan(18)]
        if self.name == "boitata":
            return [self._fan(d) for d in (-40, -20, 0, 20, 40)]
        return [self._down()]
