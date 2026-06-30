#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Localizacao e carregamento de assets.

Resolve o caminho da pasta 'asset' tanto rodando pelo codigo-fonte quanto
a partir do executavel gerado pelo PyInstaller. Tambem garante, na
inicializacao, que todas as imagens necessarias existam - regenerando as
que faltarem por meio do gerador em tools/gen_assets.py. Assim o jogo
nunca quebra por causa de um PNG ausente.
"""
import os
import sys

import pygame


def base_path():
    """Pasta base do projeto (compativel com PyInstaller)."""
    if getattr(sys, "frozen", False):
        # Executavel empacotado: assets ficam ao lado do .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ASSET_DIR = os.path.join(base_path(), "asset")

REQUIRED = (
    "hero.png", "hero_bullet.png", "saci.png", "mula.png", "boitata.png",
    "cuca.png", "monster_bullet.png", "boss_bullet.png", "et.png", "life.png",
    "bg_sky_morning.png", "bg_sky_afternoon.png", "bg_sky_night.png",
    "bg_caatinga_morning.png", "bg_caatinga_afternoon.png", "bg_caatinga_night.png",
    "menu_bg.png", "ranking_bg.png",
)


def asset(name):
    """Retorna o caminho absoluto de um arquivo dentro de 'asset'."""
    return os.path.join(ASSET_DIR, name)


def ensure_assets(win_width, win_height):
    """Gera quaisquer PNGs que estejam faltando na pasta asset."""
    missing = [f for f in REQUIRED if not os.path.exists(asset(f))]
    if not missing:
        return
    try:
        # importacao tardia para nao exigir o gerador quando os assets ja existem
        here = os.path.dirname(os.path.abspath(__file__))
        tools_dir = os.path.join(os.path.dirname(here), "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import gen_assets

        created = gen_assets.generate_all(
            ASSET_DIR, win_width, win_height, only_missing=True
        )
        if created:
            print(f"[assets] {len(created)} imagem(ns) gerada(s): {', '.join(created)}")
    except Exception as exc:  # pragma: no cover - apenas log
        print(f"[assets] aviso: nao foi possivel regenerar assets ({exc})")


def load_image(name):
    """Carrega uma imagem da pasta asset ja convertida com canal alpha."""
    return pygame.image.load(asset(name)).convert_alpha()
