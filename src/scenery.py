#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Cenario com rolagem vertical (efeito parallax).

O ceu fica parado (velocidade 0) e a caatinga rola lentamente. A camada
que rola e desenhada em duas copias empilhadas para criar um loop sem
emendas. A velocidade e passada na criacao (nao depende do nome do
arquivo), o que permite usar imagens diferentes por periodo do dia.
"""
import random

import pygame

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

    def change_image(self, name):
        from src.assets import load_image
        self.surf = load_image(f"{name}.png")


class PerspectiveGround:
    """Chao pseudo-3D no estilo Penguin Adventure (MSX, 1986).

    Versão Geométrica (Listras):
    Desenha listras alternadas coloridas baseadas na perspectiva,
    eliminando o problema de cintilação (aliasing) de texturas e 
    melhorando muito a performance. O visual fica perfeitamente
    alinhado com o estilo 8-bits original!
    """

    def __init__(self, name, speed):
        self.speed = speed
        self.distance = 0.0  # unidades virtuais já percorridas
        self.colors = self._get_colors(name)
        self._build_bands()
        self._rebuild_band_colors()

    def _get_colors(self, name):
        """Retorna uma tupla com (Cor Principal, Cor Secundária) baseada no período."""
        if "morning" in name:
            return ((190, 160, 90), (170, 140, 75))
        elif "afternoon" in name:
            return ((180, 140, 80), (160, 120, 65))
        elif "night" in name:
            return ((30, 25, 45), (40, 35, 55))
        return ((190, 160, 90), (170, 140, 75))

    def _build_bands(self):
        """Pre-calcula (y, offset de profundidade, largura) de cada faixa."""
        band_h = settings.GROUND_BAND_H
        ground_h = settings.WIN_HEIGHT - settings.HORIZON_Y
        n = ground_h // band_h
        eps = settings.GROUND_DEPTH_EPS
        z_near = 1.0 / (1.0 + eps)  # profundidade da faixa mais proxima
        self.bands = []
        for i in range(n):
            y = settings.HORIZON_Y + i * band_h
            t = (i + 1) / n                    # 0 (horizonte) -> 1 (base)
            z = 1.0 / (t + eps)
            depth_off = settings.GROUND_FOCAL * (z - z_near)
            width = round(settings.WIN_WIDTH *
                          (settings.GROUND_WIDTH_FAR +
                           (settings.GROUND_WIDTH_NEAR - settings.GROUND_WIDTH_FAR) * t))
            self.bands.append((y, depth_off, width))

    def _rebuild_band_colors(self):
        """Pre-calcula o par de cores de cada faixa, com nevoa de distancia.

        Nas faixas mais proximas do horizonte as duas cores convergem para
        a media entre elas: alem de dar profundidade atmosferica, elimina o
        flicker das listras finas ao longe (la, cada faixa de tela pula
        varias listras de uma vez e a alternancia viraria ruido).
        """
        c0, c1 = self.colors
        avg = tuple((a + b) // 2 for a, b in zip(c0, c1))
        n = len(self.bands)
        self.band_colors = []
        for i in range(n):
            t = (i + 1) / n
            if t < settings.GROUND_HAZE_T:
                f = 1.0 - t / settings.GROUND_HAZE_T  # 1 no horizonte -> 0
                h0 = tuple(round(a + (m - a) * f) for a, m in zip(c0, avg))
                h1 = tuple(round(a + (m - a) * f) for a, m in zip(c1, avg))
                self.band_colors.append((h0, h1))
            else:
                self.band_colors.append((c0, c1))

    def update(self, dt_scale=1.0):
        self.distance += self.speed * dt_scale

    def draw(self, surface):
        cx = settings.WIN_WIDTH // 2
        band_h = settings.GROUND_BAND_H

        # Fundo base (opcional, garante que tudo fique preenchido)
        pygame.draw.rect(surface, self.colors[1], (0, settings.HORIZON_Y, settings.WIN_WIDTH, settings.WIN_HEIGHT - settings.HORIZON_Y))

        for (y, depth_off, width), (c0, c1) in zip(self.bands, self.band_colors):
            # O offset de profundidade cresce para o horizonte.
            # Somado com a distância da câmera, criamos o índice da listra.
            stripe_idx = int((self.distance + depth_off) / settings.GROUND_STRIPE_DEPTH)

            # Alterna as duas cores para simular movimento contínuo
            color = c0 if stripe_idx % 2 == 0 else c1

            rect = (cx - width // 2, y, width, band_h)
            pygame.draw.rect(surface, color, rect)

    def change_image(self, name):
        """Muda o esquema de cores quando o período muda."""
        self.colors = self._get_colors(name)
        self._rebuild_band_colors()


def _depth_to_t(dist):
    """Converte distancia a frente (linhas de textura) no parametro t.

    Inverso do mapeamento usado nas faixas do PerspectiveGround: t vai de
    ~0 (horizonte) a 1 (base da tela) e passa de 1 quando o objeto ja
    "atravessou" o plano proximo e esta saindo da tela.
    """
    eps = settings.GROUND_DEPTH_EPS
    z_near = 1.0 / (1.0 + eps)
    return 1.0 / (dist / settings.GROUND_FOCAL + z_near) - eps


# paleta dos adereços por periodo (um pouco mais clara que o solo para
# os objetos em pe se destacarem do chao)
_PROP_COLORS = {
    "morning": {
        "cact_body": (78, 112, 62), "cact_hi": (104, 140, 80),
        "bush": (120, 102, 62), "bush_hi": (142, 124, 76),
        "rock": (128, 116, 98), "rock_hi": (150, 138, 118),
    },
    "afternoon": {
        "cact_body": (86, 120, 66), "cact_hi": (112, 148, 84),
        "bush": (128, 108, 64), "bush_hi": (150, 130, 78),
        "rock": (138, 124, 102), "rock_hi": (160, 146, 122),
    },
    "night": {
        "cact_body": (38, 34, 58), "cact_hi": (52, 48, 76),
        "bush": (44, 36, 56), "bush_hi": (56, 48, 70),
        "rock": (48, 42, 64), "rock_hi": (62, 56, 80),
    },
}


def _ground_shadow(s):
    """Elipse escura na base do sprite para assentar o objeto no chao."""
    w, h = s.get_size()
    shadow = pygame.Surface((w, h), pygame.SRCALPHA)
    sh = max(6, h // 8)
    pygame.draw.ellipse(shadow, (0, 0, 0, 70), (w // 6, h - sh, w - w // 3, sh))
    shadow.blit(s, (0, 0))
    return shadow


def _make_cactus(pal, tall=True):
    """Mandacaru: tronco vertical com dois bracos e nervuras claras."""
    w, h = (64, 118) if tall else (42, 66)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    body, hi = pal["cact_body"], pal["cact_hi"]
    tw = max(8, w // 4)
    trunk = pygame.Rect(w // 2 - tw // 2, h // 8, tw, h - h // 8)
    pygame.draw.rect(s, body, trunk, border_radius=tw // 2)
    arm_w = tw - 2
    # braco esquerdo (segmento horizontal + segmento vertical subindo)
    ay = h // 3
    alen = w // 4
    pygame.draw.rect(s, body, (trunk.left - alen, ay, alen + 4, arm_w),
                     border_radius=arm_w // 2)
    pygame.draw.rect(s, body, (trunk.left - alen, ay - h // 5, arm_w, h // 5 + arm_w),
                     border_radius=arm_w // 2)
    # braco direito, um pouco mais baixo
    by = h // 2
    pygame.draw.rect(s, body, (trunk.right - 4, by, alen + 4, arm_w),
                     border_radius=arm_w // 2)
    pygame.draw.rect(s, body, (trunk.right + alen - arm_w, by - h // 6,
                               arm_w, h // 6 + arm_w), border_radius=arm_w // 2)
    # nervuras do tronco
    for lx in (trunk.centerx - tw // 4, trunk.centerx + tw // 4):
        pygame.draw.line(s, hi, (lx, trunk.top + 4), (lx, trunk.bottom - 4), 1)
    return _ground_shadow(s)


def _make_bush(pal):
    """Arbusto seco da caatinga: aglomerado baixo de circulos."""
    w, h = 56, 34
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    for cx, cy, r in ((14, 24, 10), (28, 18, 13), (43, 24, 10), (22, 26, 8), (36, 26, 9)):
        pygame.draw.circle(s, pal["bush"], (cx, cy), r)
    for cx, cy, r in ((24, 15, 4), (34, 19, 3), (16, 20, 3)):
        pygame.draw.circle(s, pal["bush_hi"], (cx, cy), r)
    return _ground_shadow(s)


def _make_rock(pal):
    """Pedra achatada com um facho de luz em cima."""
    w, h = 44, 26
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(s, pal["rock"], (0, 4, w, h - 4))
    pygame.draw.ellipse(s, pal["rock_hi"], (8, 6, w // 2, h // 3))
    return _ground_shadow(s)


class GroundProp:
    """Um adereço no campo pseudo-3D: tipo + posicao lateral + distancia."""

    def __init__(self, kind, x_norm, dist, jitter, flip):
        self.kind = kind
        self.x_norm = x_norm    # -1..1 (0 = centro / ponto de fuga)
        self.dist = dist        # distancia a frente, em linhas de textura
        self.jitter = jitter    # variacao de tamanho individual
        self.flip = flip


class PropField:
    """Cactos, arbustos e pedras vindo do horizonte em pseudo-3D.

    Cada adereço nasce minusculo no ponto de fuga, desce a mesma
    "esteira" de profundidade do PerspectiveGround (mesma velocidade da
    textura) e cresce ao se aproximar, escorregando para as laterais da
    tela ate sair pelo canto inferior - como as arvores e obstaculos do
    Penguin Adventure.
    """

    KINDS = ("cactus", "cactus_small", "bush", "rock")
    WEIGHTS = (4, 3, 4, 2)

    def __init__(self, period):
        self._sprites = {}
        self.set_period(period)
        eps = settings.GROUND_DEPTH_EPS
        z_near = 1.0 / (1.0 + eps)
        # distancia em que o adereço surge (t ~ 0.015, quase no horizonte)
        self.max_dist = settings.GROUND_FOCAL * (1.0 / (0.015 + eps) - z_near)
        # ja povoa o campo em profundidades espalhadas
        self.props = [self._spawn(random.uniform(0, self.max_dist))
                      for _ in range(settings.PROP_COUNT)]

    def set_period(self, period):
        pal = _PROP_COLORS.get(period, _PROP_COLORS["night"])
        self._sprites = {
            "cactus": _make_cactus(pal, tall=True),
            "cactus_small": _make_cactus(pal, tall=False),
            "bush": _make_bush(pal),
            "rock": _make_rock(pal),
        }

    def _spawn(self, dist=None):
        kind = random.choices(self.KINDS, self.WEIGHTS)[0]
        side = random.choice((-1, 1))
        # concentra nas laterais, deixando o corredor central livre
        x_norm = side * (0.30 + random.random() ** 0.8 * 0.85)
        return GroundProp(kind, x_norm,
                          self.max_dist if dist is None else dist,
                          random.uniform(0.8, 1.2), random.random() < 0.5)

    def update(self, dt_scale=1.0):
        for i, prop in enumerate(self.props):
            prop.dist -= settings.GROUND_SPEED * dt_scale
            if _depth_to_t(prop.dist) >= 2.0:  # ja saiu por baixo da tela
                self.props[i] = self._spawn()

    def draw(self, surface):
        ground_h = settings.WIN_HEIGHT - settings.HORIZON_Y
        cx = settings.WIN_WIDTH // 2
        spread = settings.WIN_WIDTH * settings.PROP_SPREAD
        # desenha do mais distante para o mais proximo (oclusao correta)
        for prop in sorted(self.props, key=lambda p: -p.dist):
            t = _depth_to_t(prop.dist)
            if t < 0.02:
                continue
            t = min(t, 2.0)
            base = self._sprites[prop.kind]
            scale = t * prop.jitter
            w = max(1, round(base.get_width() * scale))
            h = max(1, round(base.get_height() * scale))
            img = pygame.transform.scale(base, (w, h))
            if prop.flip:
                img = pygame.transform.flip(img, True, False)
            x = cx + prop.x_norm * spread * t
            y = settings.HORIZON_Y + t * ground_h
            surface.blit(img, (round(x - w / 2), round(y - h)))


