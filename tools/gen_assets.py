#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Gerador de assets do Cordel Shooter.

Desenha todos os sprites do jogo (herói, monstros do folclore, tiros,
chefe e cenários) usando primitivas graficas do pygame e salva como
arquivos .png na pasta 'asset'.

Pode ser executado de forma independente:
    python tools/gen_assets.py

Ou chamado a partir do jogo (src/assets.py) para regenerar imagens que
estejam faltando, garantindo que o jogo sempre tenha seus recursos.
"""
import math
import os

import pygame

# ---------------------------------------------------------------------------
# Paleta de cores do tema "sertao / folclore"
# ---------------------------------------------------------------------------
TRANSP = (0, 0, 0, 0)
COURO = (140, 92, 50)          # couro do cangaceiro
COURO_ESC = (96, 60, 30)
PELE = (224, 178, 134)
AZUL_NOITE = (24, 20, 48)
AZUL_TOPO = (58, 44, 96)
LARANJA_POENTE = (232, 120, 52)
AMARELO = (250, 214, 96)
VERMELHO = (208, 56, 56)
VERDE_CUCA = (96, 150, 70)
VERDE_ESC = (60, 100, 44)
PRETO = (20, 20, 24)
BRANCO = (240, 240, 230)
ROXO = (150, 90, 200)
FOGO = (255, 150, 40)
FOGO_CLARO = (255, 220, 120)


def _new(w, h):
    return pygame.Surface((w, h), pygame.SRCALPHA)


# ---------------------------------------------------------------------------
# Sprites de personagens
# ---------------------------------------------------------------------------
def draw_hero():
    """Cangaceiro com chapeu de couro e bacamarte (aponta para cima)."""
    s = _new(48, 48)
    # corpo / gibao de couro
    pygame.draw.rect(s, COURO, (16, 20, 16, 22), border_radius=4)
    pygame.draw.rect(s, COURO_ESC, (16, 20, 16, 22), width=2, border_radius=4)
    # cartucheira cruzada
    pygame.draw.line(s, AMARELO, (16, 22), (32, 38), 3)
    # rosto
    pygame.draw.circle(s, PELE, (24, 16), 7)
    # chapeu de couro com aba curva e estrela
    pygame.draw.polygon(s, COURO_ESC, [(10, 12), (38, 12), (30, 4), (18, 4)])
    pygame.draw.ellipse(s, COURO, (8, 10, 32, 6))
    pygame.draw.circle(s, AMARELO, (24, 8), 2)
    # bacamarte apontando para cima
    pygame.draw.rect(s, PRETO, (22, 0, 4, 14))
    return s


def draw_hero_bullet():
    s = _new(8, 18)
    pygame.draw.ellipse(s, AMARELO, (0, 0, 8, 18))
    pygame.draw.ellipse(s, BRANCO, (2, 2, 4, 9))
    return s


def draw_saci():
    """Saci-Perere: figura preta, gorro vermelho, cachimbo e uma perna so."""
    s = _new(40, 44)
    # corpo
    pygame.draw.circle(s, PRETO, (20, 22), 12)
    # gorro vermelho
    pygame.draw.polygon(s, VERMELHO, [(10, 14), (30, 14), (20, 0)])
    pygame.draw.circle(s, BRANCO, (20, 0), 3)
    # olhos
    pygame.draw.circle(s, AMARELO, (16, 20), 2)
    pygame.draw.circle(s, AMARELO, (25, 20), 2)
    # cachimbo
    pygame.draw.line(s, COURO_ESC, (30, 24), (37, 22), 2)
    pygame.draw.circle(s, FOGO, (37, 22), 2)
    # uma perna so
    pygame.draw.rect(s, PRETO, (18, 33, 4, 11))
    pygame.draw.ellipse(s, COURO_ESC, (14, 41, 10, 4))
    return s


def draw_mula():
    """Mula-sem-cabeca: corpo de mula com fogo no lugar da cabeca."""
    s = _new(48, 40)
    # corpo
    pygame.draw.ellipse(s, COURO_ESC, (8, 14, 30, 16))
    # pernas
    for x in (12, 20, 28, 34):
        pygame.draw.rect(s, PRETO, (x, 28, 3, 10))
    # rabo
    pygame.draw.line(s, PRETO, (8, 18), (2, 14), 2)
    # pescoco
    pygame.draw.polygon(s, COURO_ESC, [(34, 16), (44, 8), (40, 20)])
    # fogo no lugar da cabeca
    pygame.draw.polygon(s, FOGO, [(38, 12), (48, 0), (44, 14)])
    pygame.draw.polygon(s, FOGO_CLARO, [(40, 12), (45, 4), (43, 13)])
    return s


def draw_boitata():
    """Boitata: serpente de fogo ondulada."""
    s = _new(48, 36)
    pts_top = []
    pts_bot = []
    for i in range(0, 49, 4):
        y = 18 + math.sin(i / 5.0) * 8
        pts_top.append((i, y - 6))
        pts_bot.append((i, y + 6))
    poly = pts_top + pts_bot[::-1]
    pygame.draw.polygon(s, FOGO, poly)
    pygame.draw.polygon(s, FOGO_CLARO, [(p[0], p[1] + 2) for p in pts_top] +
                        [(p[0], p[1] - 2) for p in pts_bot[::-1]])
    # cabeca
    pygame.draw.circle(s, FOGO, (4, int(18 + math.sin(0) * 8)), 6)
    pygame.draw.circle(s, VERMELHO, (4, 18), 2)
    return s


def draw_cuca():
    """Cuca: bruxa-jacare, chefe da fase."""
    s = _new(120, 100)
    # corpo / vestido
    pygame.draw.polygon(s, ROXO, [(40, 96), (80, 96), (72, 50), (48, 50)])
    # cabeca de jacare verde
    pygame.draw.ellipse(s, VERDE_CUCA, (28, 18, 64, 44))
    pygame.draw.ellipse(s, VERDE_ESC, (28, 18, 64, 44), width=3)
    # focinho
    pygame.draw.ellipse(s, VERDE_CUCA, (40, 44, 40, 22))
    # boca e dentes
    pygame.draw.rect(s, PRETO, (42, 54, 36, 6))
    for i in range(43, 78, 6):
        pygame.draw.polygon(s, BRANCO, [(i, 54), (i + 5, 54), (i + 2, 60)])
    # olhos amarelos
    pygame.draw.circle(s, AMARELO, (48, 34), 7)
    pygame.draw.circle(s, AMARELO, (72, 34), 7)
    pygame.draw.circle(s, PRETO, (48, 34), 3)
    pygame.draw.circle(s, PRETO, (72, 34), 3)
    # cabelo de fogo
    for x in range(28, 93, 10):
        pygame.draw.polygon(s, FOGO, [(x, 22), (x + 10, 22), (x + 5, 4)])
    # garras
    pygame.draw.polygon(s, AMARELO, [(28, 70), (40, 64), (34, 80)])
    pygame.draw.polygon(s, AMARELO, [(92, 70), (80, 64), (86, 80)])
    return s


def draw_monster_bullet():
    s = _new(12, 12)
    pygame.draw.circle(s, ROXO, (6, 6), 6)
    pygame.draw.circle(s, BRANCO, (6, 6), 2)
    return s


def draw_boss_bullet():
    s = _new(18, 18)
    pygame.draw.circle(s, VERDE_ESC, (9, 9), 9)
    pygame.draw.circle(s, VERDE_CUCA, (9, 9), 6)
    pygame.draw.circle(s, FOGO_CLARO, (9, 9), 2)
    return s


# ---------------------------------------------------------------------------
# Cenarios
# ---------------------------------------------------------------------------
def _gradient(w, h, top, bottom):
    s = _new(w, h)
    for y in range(h):
        t = y / max(1, h - 1)
        col = (int(top[0] + (bottom[0] - top[0]) * t),
               int(top[1] + (bottom[1] - top[1]) * t),
               int(top[2] + (bottom[2] - top[2]) * t))
        pygame.draw.line(s, col, (0, y), (w, y))
    return s


def draw_sky(w, h):
    """Ceu de poente do sertao com estrelas."""
    s = _gradient(w, h, AZUL_TOPO, LARANJA_POENTE)
    # estrelas
    import random
    rng = random.Random(7)
    for _ in range(70):
        x = rng.randint(0, w)
        y = rng.randint(0, int(h * 0.55))
        r = rng.choice((1, 1, 2))
        pygame.draw.circle(s, BRANCO, (x, y), r)
    # lua
    pygame.draw.circle(s, AMARELO, (int(w * 0.78), int(h * 0.18)), 26)
    pygame.draw.circle(s, LARANJA_POENTE, (int(w * 0.74), int(h * 0.16)), 22)
    return s


def draw_caatinga(w, h):
    """Camada de silhueta da caatinga (mandacarus e morros) com fundo transparente."""
    s = _new(w, h)
    base = h - 90
    pygame.draw.polygon(s, AZUL_NOITE,
                        [(0, h), (0, base), (w * 0.2, base - 30),
                         (w * 0.45, base + 10), (w * 0.7, base - 40),
                         (w, base), (w, h)])
    # mandacarus (cactos)
    for cx in range(60, w, 150):
        pygame.draw.rect(s, PRETO, (cx, base - 40, 8, 50))
        pygame.draw.rect(s, PRETO, (cx - 10, base - 24, 8, 18))
        pygame.draw.rect(s, PRETO, (cx + 10, base - 30, 8, 22))
    return s


def draw_menu_bg(w, h):
    s = draw_sky(w, h)
    s.blit(draw_caatinga(w, h), (0, 0))
    # faixa decorativa de cordel no topo
    pygame.draw.rect(s, AZUL_NOITE, (0, 0, w, 6))
    pygame.draw.rect(s, AMARELO, (0, 6, w, 2))
    return s


def draw_ranking_bg(w, h):
    s = _gradient(w, h, AZUL_NOITE, AZUL_TOPO)
    pygame.draw.rect(s, AMARELO, (0, 0, w, 4))
    pygame.draw.rect(s, AMARELO, (0, h - 4, w, 4))
    return s


# ---------------------------------------------------------------------------
# Orquestracao
# ---------------------------------------------------------------------------
def generate_all(asset_dir, win_width=800, win_height=600, only_missing=False):
    """Gera todos os PNGs em asset_dir. Retorna a lista de arquivos criados."""
    if not pygame.get_init():
        pygame.init()

    os.makedirs(asset_dir, exist_ok=True)

    builders = {
        "hero.png": draw_hero,
        "hero_bullet.png": draw_hero_bullet,
        "saci.png": draw_saci,
        "mula.png": draw_mula,
        "boitata.png": draw_boitata,
        "cuca.png": draw_cuca,
        "monster_bullet.png": draw_monster_bullet,
        "boss_bullet.png": draw_boss_bullet,
        "bg_sky.png": lambda: draw_sky(win_width, win_height),
        "bg_caatinga.png": lambda: draw_caatinga(win_width, win_height),
        "menu_bg.png": lambda: draw_menu_bg(win_width, win_height),
        "ranking_bg.png": lambda: draw_ranking_bg(win_width, win_height),
    }

    created = []
    for filename, builder in builders.items():
        path = os.path.join(asset_dir, filename)
        if only_missing and os.path.exists(path):
            continue
        surface = builder()
        pygame.image.save(surface, path)
        created.append(filename)
    return created


if __name__ == "__main__":
    # quando executado isoladamente (ex.: no build), permite rodar sem monitor
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    here = os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.join(os.path.dirname(here), "asset")
    files = generate_all(asset_path)
    print(f"{len(files)} assets gerados em: {asset_path}")
    for f in files:
        print("  -", f)
