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
from src.specials import ET


class Spawner:
    @staticmethod
    def background():
        """Monta o cenario do periodo atual (manha/tarde/noite, pelo relogio).
        Ceu parado + nuvens rolando (parallax) + chao da caatinga rolando."""
        period = settings.current_period()
        sky = f"bg_sky_{period}"
        clouds = f"bg_clouds_{period}"
        caatinga = f"bg_caatinga_{period}"
        h = settings.WIN_HEIGHT
        return [
            Scenery(sky, 0, 0),
            Scenery(clouds, 0.4, 0),
            Scenery(clouds, 0.4, -h),
            Scenery(caatinga, settings.CAATINGA_SPEED, 0),
            Scenery(caatinga, settings.CAATINGA_SPEED, -h),
        ]


    @staticmethod
    def et():
        """Cria o ET de Varginha entrando por um dos lados da tela."""
        h = settings.WIN_HEIGHT
        side = random.choice((-1, 1))
        x = -30 if side == 1 else settings.WIN_WIDTH + 30
        y = random.randint(60, int(h * 0.4))
        return ET((x, y), settings.SPEED[settings.ET] * side)


    @staticmethod
    def hero():
        return Hero((settings.WIN_WIDTH // 2, settings.WIN_HEIGHT - 60))

    @staticmethod
    def random_monster():
        name = random.choice(settings.MONSTERS)
        # Margens calculadas com base na amplitude de oscilação e largura do sprite:
        # Saci (amp=26, larg=40 -> margem=46), Boitatá (amp=44, larg=48 -> margem=68)
        margins = {"saci": 50, "mula": 35, "boitata": 75}
        margin = margins.get(name, 40)
        x = random.randint(margin, settings.WIN_WIDTH - margin)
        # Nace totalmente fora da tela (y = -30 garante bottom <= 0 para todos)
        return Monster(name, (x, -30))


    @staticmethod
    def boss():
        return Boss((settings.WIN_WIDTH // 2, -60))
