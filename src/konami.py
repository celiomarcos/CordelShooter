#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Detector do codigo Konami: CIMA CIMA BAIXO BAIXO ESQ DIR ESQ DIR B A.

Recebe teclas (eventos KEYDOWN) uma a uma e devolve True no exato
momento em que a sequencia completa e digitada na ordem certa.
"""
import pygame


class KonamiCode:
    SEQUENCE = [
        pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
        pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT,
        pygame.K_b, pygame.K_a,
    ]

    def __init__(self):
        self.index = 0

    def push(self, key):
        """Alimenta uma tecla. Retorna True se completou a sequencia."""
        if key == self.SEQUENCE[self.index]:
            self.index += 1
            if self.index == len(self.SEQUENCE):
                self.index = 0
                return True
        else:
            # recomeca; se a tecla ja casa com o inicio, conta como passo 1
            self.index = 1 if key == self.SEQUENCE[0] else 0
        return False
