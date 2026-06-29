#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Cenario com rolagem vertical (efeito parallax).

Cada camada e desenhada duas vezes, empilhada verticalmente, e desliza
para baixo para dar sensacao de movimento. A camada do ceu fica parada
(velocidade 0) e a caatinga rola lentamente.
"""
from src import settings
from src.entity import Entity


class Scenery(Entity):
    def __init__(self, name, offset_y):
        # posicao inicial: a imagem ocupa a tela inteira; offset empilha copias
        super().__init__(name, (settings.WIN_WIDTH // 2, settings.WIN_HEIGHT // 2))
        self.rect.top = offset_y

    def update(self):
        if self.speed == 0:
            return
        self.rect.y += self.speed
        # quando a copia sai por baixo, reposiciona acima da outra
        if self.rect.top >= settings.WIN_HEIGHT:
            self.rect.bottom = 0
