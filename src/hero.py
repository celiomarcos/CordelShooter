#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Heroi controlado pelo jogador (o cangaceiro).

Move-se em todas as direcoes dentro da janela usando setas ou WASD e
atira para cima com a barra de espaco, respeitando uma cadencia minima.
"""
import pygame

from src import settings
from src.bullet import HeroBullet
from src.entity import Entity


class Hero(Entity):
    def __init__(self, position):
        super().__init__(settings.HERO, position)
        self.cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()
        up = keys[pygame.K_UP] or keys[pygame.K_w]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if down and self.rect.bottom < settings.WIN_HEIGHT:
            self.rect.y += self.speed
        if left and self.rect.left > 0:
            self.rect.x -= self.speed
        if right and self.rect.right < settings.WIN_WIDTH:
            self.rect.x += self.speed

        if self.cooldown > 0:
            self.cooldown -= 1

    def try_shoot(self):
        """Retorna um HeroBullet se a tecla de tiro estiver pressionada e
        a cadencia permitir; caso contrario retorna None."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            self.cooldown = settings.SHOOT_COOLDOWN[self.name]
            return HeroBullet((self.rect.centerx, self.rect.top))
        return None
