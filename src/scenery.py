#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Cenario com rolagem vertical (efeito parallax).

O ceu fica parado (velocidade 0) e a caatinga rola lentamente. A camada
que rola e desenhada em duas copias empilhadas para criar um loop sem
emendas. A velocidade e passada na criacao (nao depende do nome do
arquivo), o que permite usar imagens diferentes por periodo do dia.
"""
from src import settings
from src.entity import Entity


class Scenery(Entity):
    def __init__(self, name, speed, offset_y):
        # a imagem ocupa a tela inteira; offset_y empilha copias
        super().__init__(name, (settings.WIN_WIDTH // 2, settings.WIN_HEIGHT // 2))
        self.speed = speed
        self.rect.top = offset_y

    def update(self, dt_scale=1.0):
        if self.speed == 0:
            return
        self.rect.y += round(self.speed * dt_scale)
        # quando a copia sai por baixo, reposiciona acima da outra
        if self.rect.top >= settings.WIN_HEIGHT:
            self.rect.bottom = 0

