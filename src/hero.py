#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Heroi controlado pelo jogador (o cangaceiro).

Move-se em todas as direcoes dentro da janela usando setas ou WASD e
atira para cima com a barra de espaco, respeitando uma cadencia minima.
"""
import pygame

from src import settings, sounds
from src.bullet import HeroBullet
from src.entity import Entity


class Hero(Entity):

    def __init__(self, position):
        super().__init__(settings.HERO, position)
        self.cooldown = 0
        self.cangaco = False  # Modo Cangaco (easter egg): tiro triplo
        self.invincible_timer = 0

    @property
    def is_invincible(self):
        return self.invincible_timer > 0

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

        if self.invincible_timer > 0:
            self.invincible_timer -= 1


    def try_shoot(self):
        """Retorna a lista de tiros disparados neste frame (vazia se nao
        atirou). No Modo Cangaco dispara um tiro triplo e mais rapido."""
        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_SPACE] and self.cooldown == 0):
            return []
        sounds.play_sound("shoot")
        cx, ty = self.rect.centerx, self.rect.top
        if self.cangaco:
            self.cooldown = max(4, settings.SHOOT_COOLDOWN[self.name] // 2)
            return [HeroBullet((cx - 16, ty)), HeroBullet((cx, ty)),
                    HeroBullet((cx + 16, ty))]
        self.cooldown = settings.SHOOT_COOLDOWN[self.name]
        return [HeroBullet((cx, ty))]

