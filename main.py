#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Ponto de entrada do Cordel Shooter - Lendas do Sertao.

Execute com:  python main.py
"""
import os

# Set environment variable to hide the greeting
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys

# garante que a raiz do projeto esteja no caminho de importacao
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import Game


def main():
    Game().run()


if __name__ == "__main__":
    main()
