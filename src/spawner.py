#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Fabrica de entidades (padrao Factory).

Centraliza a criacao de herois, monstros, chefe e cenario. O restante
do codigo pede entidades pelo nome, sem conhecer os detalhes de
construcao de cada classe.
"""
import random

from src import settings
from src.boss import Boss
from src.hero import Hero
from src.monster import Monster
from src.scenery import Scenery


class Spawner:
    @staticmethod
    def background():
        """Monta o cenario do periodo atual (manha/tarde/noite, pelo relogio).
        Ceu parado ao fundo + caatinga rolando em duas copias (parallax)."""
        period = settings.current_period()
        sky = f"bg_sky_{period}"
        caatinga = f"bg_caatinga_{period}"
        h = settings.WIN_HEIGHT
        return [
            Scenery(sky, 0, 0),
            Scenery(caatinga, settings.CAATINGA_SPEED, 0),
            Scenery(caatinga, settings.CAATINGA_SPEED, -h),
        ]

    @staticmethod
    def et():
        """Cria o ET de Varginha entrando por um dos lados da tela."""
        import random as _r
        h = settings.WIN_HEIGHT
        side = _r.choice((-1, 1))
        x = -30 if side == 1 else settings.WIN_WIDTH + 30
        y = _r.randint(60, int(h * 0.4))
        from src.specials import ET
        return ET((x, y), settings.SPEED[settings.ET] * side)

    @staticmethod
    def hero():
        return Hero((settings.WIN_WIDTH // 2, settings.WIN_HEIGHT - 60))

    @staticmethod
    def random_monster():
        name = random.choice(settings.MONSTERS)
        x = random.randint(40, settings.WIN_WIDTH - 40)
        return Monster(name, (x, -20))

    @staticmethod
    def boss():
        return Boss((settings.WIN_WIDTH // 2, -60))
