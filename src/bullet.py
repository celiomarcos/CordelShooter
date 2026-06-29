#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Projeteis do jogo.

HeroBullet sobe pela tela (tiro do cangaceiro). MonsterBullet e
BossBullet descem em direcao ao heroi. Todos herdam de Entity.
"""
from src import settings
from src.entity import Entity


class HeroBullet(Entity):
    """Tiro do heroi: viaja para cima."""

    def __init__(self, position):
        super().__init__(settings.HERO_BULLET, position)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.health = 0


class MonsterBullet(Entity):
    """Tiro dos monstros: viaja para baixo."""

    def __init__(self, position, name=settings.MONSTER_BULLET):
        super().__init__(name, position)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > settings.WIN_HEIGHT:
            self.health = 0


class BossBullet(MonsterBullet):
    """Tiro do chefe: mais forte, tambem desce."""

    def __init__(self, position):
        super().__init__(position, name=settings.BOSS_BULLET)
