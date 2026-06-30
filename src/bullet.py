#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Projeteis do jogo.

HeroBullet sobe em linha reta. Os tiros inimigos (MonsterBullet e
BossBullet) usam um vetor de velocidade (vx, vy), o que permite tiros
retos, diagonais, em leque ou mirados no heroi. A posicao e guardada em
ponto flutuante para que trajetorias diagonais fiquem suaves.
"""
from src import settings
from src.entity import Entity


class HeroBullet(Entity):
    """Tiro do heroi: viaja para cima em linha reta."""

    def __init__(self, position):
        super().__init__(settings.HERO_BULLET, position)

    def update(self, dt_scale=1.0):
        self.rect.y -= round(self.speed * dt_scale)
        if self.rect.bottom < 0:
            self.health = 0


class MonsterBullet(Entity):
    """Tiro inimigo com vetor de velocidade.

    velocity = (vx, vy). Se vy for None, usa a velocidade padrao da
    entidade (descendo em linha reta).
    """

    def __init__(self, position, velocity=(0, None), name=settings.MONSTER_BULLET):
        super().__init__(name, position)
        vx, vy = velocity
        self.vx = float(vx)
        self.vy = float(vy if vy is not None else self.speed)
        self._fx = float(self.rect.centerx)
        self._fy = float(self.rect.centery)

    def update(self, dt_scale=1.0):
        self._fx += self.vx * dt_scale
        self._fy += self.vy * dt_scale
        self.rect.center = (round(self._fx), round(self._fy))
        # morre ao sair por qualquer borda da tela
        if (self.rect.top > settings.WIN_HEIGHT or self.rect.bottom < 0 or
                self.rect.right < 0 or self.rect.left > settings.WIN_WIDTH):
            self.health = 0



class BossBullet(MonsterBullet):
    """Tiro do chefe: mais forte; tambem usa vetor de velocidade."""

    def __init__(self, position, velocity=(0, None)):
        super().__init__(position, velocity, name=settings.BOSS_BULLET)
