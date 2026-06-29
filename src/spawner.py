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
        """Retorna as camadas de cenario (duas copias de cada para rolagem)."""
        layers = []
        for name in settings.BACKGROUNDS:
            layers.append(Scenery(name, 0))
            layers.append(Scenery(name, -settings.WIN_HEIGHT))
        return layers

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
