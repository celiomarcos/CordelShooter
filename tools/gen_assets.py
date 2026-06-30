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
import random

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
def _lerp(c1, c2, t):
    return (int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t))


def _vgradient(w, h, stops):
    """Gradiente vertical com varias paradas: stops = [(pos0a1, cor), ...]."""
    s = _new(w, h)
    stops = sorted(stops)
    for y in range(h):
        t = y / max(1, h - 1)
        lo, hi = stops[0], stops[-1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                lo, hi = stops[i], stops[i + 1]
                break
        span = (hi[0] - lo[0]) or 1
        pygame.draw.line(s, _lerp(lo[1], hi[1], (t - lo[0]) / span), (0, y), (w, y))
    return s


def _hills(s, w, h, far_col, near_col):
    base = 300
    far = [(x, base - 15 + int(math.sin(x / 120.0) * 8)) for x in range(0, w + 40, 40)]
    pygame.draw.polygon(s, far_col, [(0, base)] + far + [(w, base)])
    near = [(x, base - 6 + int(math.sin(x / 90.0 + 1.5) * 6)) for x in range(0, w + 40, 40)]
    pygame.draw.polygon(s, near_col, [(0, base)] + near + [(w, base)])


def _sun(s, cx, cy, color):
    for r, a in ((72, 40), (54, 60), (40, 95)):
        halo = _new(2 * r, 2 * r)
        pygame.draw.circle(halo, (color[0], color[1], color[2], a), (r, r), r)
        s.blit(halo, (cx - r, cy - r))
    pygame.draw.circle(s, color, (cx, cy), 30)


def _clouds(s, w, h, color, n, ylo=0.16, yhi=0.5, seed=3):
    rng = random.Random(seed)
    for _ in range(n):
        cw, ch = rng.randint(120, 250), rng.randint(22, 42)
        cloud = _new(cw, ch)
        pygame.draw.ellipse(cloud, color, (0, 0, cw, ch))
        s.blit(cloud, (rng.randint(-40, w), rng.randint(int(h * ylo), int(h * yhi))))


def draw_sky(w, h, period="night"):
    """Ceu do sertao conforme o periodo do dia (manha, tarde ou noite)."""
    if period == "morning":
        s = _vgradient(w, h, [
            (0.00, (126, 176, 224)), (0.50, (196, 214, 228)),
            (0.78, (255, 214, 150)), (1.00, (150, 150, 120)),
        ])
        _sun(s, int(w * 0.76), int(h * 0.34), (255, 236, 170))
        _hills(s, w, h, (96, 120, 86), (70, 96, 64))
        return s
    if period == "afternoon":
        s = _vgradient(w, h, [
            (0.00, (74, 140, 214)), (0.50, (150, 194, 234)),
            (0.82, (232, 226, 196)), (1.00, (150, 150, 120)),
        ])
        _sun(s, int(w * 0.30), int(h * 0.16), (255, 250, 224))
        _hills(s, w, h, (84, 112, 82), (58, 86, 60))
        return s

    # noite (padrao): gradiente escuro, via-lactea, estrelas, lua, morros
    s = _vgradient(w, h, [
        (0.00, (12, 12, 42)), (0.42, (44, 32, 88)),
        (0.68, (138, 74, 92)), (0.82, (238, 150, 74)), (1.00, (74, 40, 44)),
    ])
    rng = random.Random(7)
    for _ in range(150):  # via-lactea
        x = rng.randint(0, w)
        y = int(h * 0.10 + (x / w) * h * 0.16 + rng.randint(-16, 16))
        if 0 <= y < int(h * 0.6):
            pygame.draw.circle(s, (200, 200, 255), (x, y), 1)
    for _ in range(130):  # estrelas
        x, y = rng.randint(0, w), rng.randint(0, int(h * 0.62))
        size = rng.choice((1, 1, 1, 2, 2, 3))
        col = rng.choice([(240, 240, 230), (255, 240, 200), (200, 210, 255)])
        pygame.draw.circle(s, col, (x, y), size)
        if size == 3:
            glow = _new(10, 10)
            pygame.draw.circle(glow, (255, 255, 220, 70), (5, 5), 5)
            s.blit(glow, (x - 5, y - 5))
    mx, my = int(w * 0.78), int(h * 0.20)  # lua
    for r, a in ((56, 26), (44, 38), (32, 58)):
        halo = _new(2 * r, 2 * r)
        pygame.draw.circle(halo, (255, 245, 200, a), (r, r), r)
        s.blit(halo, (mx - r, my - r))
    pygame.draw.circle(s, (248, 242, 205), (mx, my), 24)
    for cx, cy, cr in ((mx - 8, my - 6, 4), (mx + 6, my + 5, 6), (mx + 2, my - 10, 3)):
        pygame.draw.circle(s, (228, 220, 178), (cx, cy), cr)
    _hills(s, w, h, (40, 30, 58), (26, 20, 40))
    return s


def draw_clouds(w, h, period="night"):
    """Nuvens roláveis (em parallax) conforme o período do dia."""
    s = _new(w, h)
    if period == "morning":
        _clouds(s, w, h, (255, 255, 255, 90), 4, ylo=0.05, yhi=0.95, seed=12)
    elif period == "afternoon":
        _clouds(s, w, h, (255, 255, 255, 110), 4, ylo=0.05, yhi=0.95, seed=15)
    else:  # night
        _clouds(s, w, h, (60, 40, 70, 70), 3, ylo=0.05, yhi=0.95, seed=7)
    return s


_CAATINGA_COLORS = {
    "morning": {"ridge": (70, 84, 58), "base": (52, 64, 44), "cact": (46, 58, 40), "bush": (58, 70, 48)},
    "afternoon": {"ridge": (76, 92, 62), "base": (56, 70, 48), "cact": (50, 64, 44), "bush": (62, 76, 52)},
    "night": {"ridge": (20, 16, 30), "base": (14, 11, 22), "cact": (12, 10, 18), "bush": (16, 13, 24)},
}


def draw_caatinga(w, h, period="night"):
    """Solo da caatinga sólido (sem transparência) com cactos e arbustos
    distribuídos por toda a altura (seamless para rolagem infinita)."""
    col = _CAATINGA_COLORS.get(period, _CAATINGA_COLORS["night"])
    s = _new(w, h)
    # Preenche o fundo completamente com a cor do chão
    s.fill(col["base"])

    rng = random.Random(13)
    cact = col["cact"]
    # Espalha cactos de forma contínua
    for cy in range(30, h, 80):
        for _ in range(2):
            cx = rng.randint(40, w - 40)
            ht = rng.randint(34, 55)
            top = cy - ht
            pygame.draw.rect(s, cact, (cx, top, 8, ht))
            if rng.random() < 0.7:
                ay = top + rng.randint(8, 18)
                pygame.draw.rect(s, cact, (cx - 10, ay, 8, 14))
                pygame.draw.rect(s, cact, (cx - 10, ay - 4, 4, 6))
            if rng.random() < 0.7:
                by = top + rng.randint(8, 18)
                pygame.draw.rect(s, cact, (cx + 8, by, 8, 14))
                pygame.draw.rect(s, cact, (cx + 12, by - 4, 4, 6))

    # Espalha arbustos secos por todo o solo
    for _ in range(16):
        cx = rng.randint(10, w - 10)
        cy = rng.randint(10, h - 10)
        pygame.draw.circle(s, col["bush"], (cx, cy), rng.randint(5, 10))

    return s



def draw_et():
    """ET de Varginha: cabeca grande, tres protuberancias e olhos vermelhos."""
    s = _new(40, 46)
    body = (120, 140, 90)
    pygame.draw.ellipse(s, body, (12, 24, 16, 18))          # tronco
    pygame.draw.rect(s, body, (15, 40, 4, 6))               # pernas
    pygame.draw.rect(s, body, (22, 40, 4, 6))
    pygame.draw.line(s, body, (13, 28), (4, 34), 3)         # bracos
    pygame.draw.line(s, body, (27, 28), (36, 34), 3)
    pygame.draw.ellipse(s, body, (8, 2, 24, 28))            # cabeca
    for bx in (13, 20, 27):                                 # protuberancias
        pygame.draw.circle(s, body, (bx, 4), 3)
    pygame.draw.ellipse(s, (200, 40, 40), (12, 12, 7, 11))  # olhos
    pygame.draw.ellipse(s, (200, 40, 40), (21, 12, 7, 11))
    pygame.draw.ellipse(s, (255, 170, 170), (13, 13, 3, 4))
    pygame.draw.ellipse(s, (255, 170, 170), (22, 13, 3, 4))
    return s


def draw_life():
    """Coracao do bonus de vida."""
    s = _new(24, 22)
    red = (230, 60, 80)
    pygame.draw.circle(s, red, (7, 8), 6)
    pygame.draw.circle(s, red, (17, 8), 6)
    pygame.draw.polygon(s, red, [(1, 10), (23, 10), (12, 21)])
    pygame.draw.circle(s, (255, 180, 190), (6, 6), 2)
    return s


def draw_menu_bg(w, h):
    s = draw_sky(w, h)
    s.blit(draw_caatinga(w, h), (0, 0))
    # molduras de cordel (faixas + furos amarelos)
    pygame.draw.rect(s, (20, 16, 40), (0, 0, w, 8))
    pygame.draw.rect(s, (20, 16, 40), (0, h - 8, w, 8))
    pygame.draw.rect(s, AMARELO, (0, 8, w, 2))
    pygame.draw.rect(s, AMARELO, (0, h - 10, w, 2))
    for x in range(0, w, 28):
        pygame.draw.circle(s, AMARELO, (x, 4), 2)
        pygame.draw.circle(s, AMARELO, (x, h - 4), 2)
    return s


def draw_ranking_bg(w, h):
    s = _vgradient(w, h, [(0.0, (16, 14, 34)), (1.0, (42, 30, 72))])
    rng = random.Random(21)
    for _ in range(60):
        pygame.draw.circle(s, (180, 180, 210),
                           (rng.randint(0, w), rng.randint(0, h)), 1)
    pygame.draw.rect(s, AMARELO, (0, 0, w, 4))
    pygame.draw.rect(s, AMARELO, (0, h - 4, w, 4))
    pygame.draw.rect(s, AMARELO, (20, 20, w - 40, h - 40), 2)
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
        "et.png": draw_et,
        "life.png": draw_life,
        "menu_bg.png": lambda: draw_menu_bg(win_width, win_height),
        "ranking_bg.png": lambda: draw_ranking_bg(win_width, win_height),
    }
    # ceu, caatinga e nuvens por periodo do dia (manha / tarde / noite)
    for period in ("morning", "afternoon", "night"):
        builders[f"bg_sky_{period}.png"] = \
            (lambda p: lambda: draw_sky(win_width, win_height, p))(period)
        builders[f"bg_caatinga_{period}.png"] = \
            (lambda p: lambda: draw_caatinga(win_width, win_height, p))(period)
        builders[f"bg_clouds_{period}.png"] = \
            (lambda p: lambda: draw_clouds(win_width, win_height, p))(period)


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
