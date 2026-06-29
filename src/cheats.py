#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Estado global de easter eggs / trapacas do jogo.

Mantido como um unico objeto compartilhado para que o Menu (onde o
codigo secreto e digitado) consiga sinalizar a fase (World) sem
acoplamento direto entre as classes.
"""


class _Cheats:
    def __init__(self):
        self.cangaco = False  # Modo Cangaco: vida extra + tiro triplo


CHEATS = _Cheats()
