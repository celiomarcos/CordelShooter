#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Gerenciador de nuvens procedurais dinâmicas.

Gera nuvens individuais como elipses suavizadas em tempo de execução e gerencia
sua movimentação e ressurgimento na tela, criando um efeito de parallax e
dinâmica visual tanto no menu principal quanto na fase de jogo.
"""
import random
import pygame
from src import settings


class DynamicCloud:
    def __init__(self, x, y, width, height, speed, alpha, color_base):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.alpha = alpha
        self.color_base = color_base
        self.surf = None
        self._recreate_surf()

    def _recreate_surf(self):
        # Cria uma superfície com canal alpha e desenha a elipse da nuvem
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        color = (self.color_base[0], self.color_base[1], self.color_base[2], self.alpha)
        pygame.draw.ellipse(self.surf, color, (0, 0, self.width, self.height))

    def update(self, dt_scale):
        # As nuvens descem em direção ao horizonte
        self.y += self.speed * dt_scale
        if self.y > settings.HORIZON_Y:
            self.y = -self.height
            self.x = random.randint(-60, settings.WIN_WIDTH)
            self.speed = random.uniform(0.3, 0.7)

    def draw(self, surface):
        surface.blit(self.surf, (round(self.x), round(self.y)))


class CloudSystem:
    def __init__(self):
        self.clouds = []

    def setup(self, period):
        self.clouds.clear()
        # Define a opacidade e tonalidade conforme o período do dia
        if period == "morning":
            color = (255, 255, 255)
            alpha = 95
        elif period == "afternoon":
            color = (255, 255, 255)
            alpha = 115
        else:  # night
            color = (60, 40, 70)
            alpha = 80

        # Cria 5 nuvens distribuídas na tela em alturas aleatórias
        for _ in range(5):
            w = random.randint(120, 240)
            h = random.randint(22, 40)
            x = random.randint(-60, settings.WIN_WIDTH)
            y = random.randint(-40, 260)
            speed = random.uniform(0.3, 0.6)
            self.clouds.append(DynamicCloud(x, y, w, h, speed, alpha, color))

    def update(self, dt_scale=1.0):
        for cloud in self.clouds:
            cloud.update(dt_scale)

    def draw(self, surface):
        for cloud in self.clouds:
            cloud.draw(surface)
