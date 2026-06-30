#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Menu principal e tela de ranking.

O menu exibe o titulo, as opcoes navegaveis e - conforme exigido pela
atividade - os comandos de controle do jogo ja na primeira tela.
"""
import sys

import pygame

from src import hud, settings
from src.assets import load_image
from src.cheats import CHEATS
from src.konami import KonamiCode
from src.ranking import ScoreDB


class Menu:
    def __init__(self, window):
        self.window = window
        self.bg = load_image("menu_bg.png")
        self.ranking_bg = load_image("ranking_bg.png")
        self.selected = 0
        self.konami = KonamiCode()
        self._flash = 0  # frames restantes da mensagem do easter egg

    # ------------------------------------------------------------------
    def run(self):
        """Loop do menu. Retorna a opcao escolhida pelo jogador."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(settings.FPS)
            self._draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # easter egg: codigo Konami
                    if self.konami.push(event.key):
                        CHEATS.cangaco = True
                        self._flash = 210
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected = (self.selected + 1) % len(settings.MENU_OPTIONS)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.selected = (self.selected - 1) % len(settings.MENU_OPTIONS)
                    elif event.key == pygame.K_RETURN:
                        return settings.MENU_OPTIONS[self.selected]
                    elif event.key == pygame.K_ESCAPE:
                        return settings.MENU_EXIT

    def _draw(self):
        self.window.blit(self.bg, (0, 0))
        cx = settings.WIN_WIDTH // 2
        hud.draw_text(self.window, "CORDEL SHOOTER", 56, settings.COLOR_YELLOW,
                      center=(cx, 90), bold=True)
        hud.draw_text(self.window, "Lendas do Sertao", 26, settings.COLOR_WHITE,
                      center=(cx, 135))

        for i, option in enumerate(settings.MENU_OPTIONS):
            color = settings.COLOR_ORANGE if i == self.selected else settings.COLOR_WHITE
            label = f"> {option} <" if i == self.selected else option
            hud.draw_text(self.window, label, 30, color, center=(cx, 240 + i * 48))

        # Comandos de controle (exigencia da atividade)
        box_y = settings.WIN_HEIGHT - 140
        pygame.draw.rect(self.window, settings.COLOR_DARK,
                         (cx - 230, box_y - 10, 460, 110), border_radius=8)
        hud.draw_text(self.window, "CONTROLES", 20, settings.COLOR_YELLOW,
                      center=(cx, box_y + 6), bold=True)
        for i, line in enumerate(settings.CONTROLS_TEXT):
            hud.draw_text(self.window, line, 18, settings.COLOR_WHITE,
                          center=(cx, box_y + 34 + i * 24))

        # credito discreto do desenvolvedor (acima da moldura de cordel)
        hud.draw_text(self.window, "developed by celiomarcos@gmail.com  - Uninter RU 5233696",
                      
                      13, (170, 170, 182), center=(cx, settings.WIN_HEIGHT - 24))

        # mensagem do easter egg (Modo Cangaco)
        if self._flash > 0 or CHEATS.cangaco:
            if self._flash > 0:
                hud.draw_text(self.window, "* MODO CANGACO ATIVADO! *", 24,
                              settings.COLOR_YELLOW, center=(cx, 180), bold=True)
                self._flash -= 1
            else:
                hud.draw_text(self.window, "Modo Cangaco ativo", 14,
                              settings.COLOR_ORANGE, center=(cx, 165))
        pygame.display.flip()

    # ------------------------------------------------------------------
    def show_ranking(self):
        db = ScoreDB()
        rows = db.top()
        db.close()
        clock = pygame.time.Clock()
        while True:
            clock.tick(settings.FPS)
            self.window.blit(self.ranking_bg, (0, 0))
            cx = settings.WIN_WIDTH // 2
            hud.draw_text(self.window, "TOP 10 - RANKING", 40,
                          settings.COLOR_YELLOW, center=(cx, 60), bold=True)
            hud.draw_text(self.window, "NOME", 20, settings.COLOR_ORANGE, topleft=(cx - 200, 120), bold=True)
            hud.draw_text(self.window, "PONTOS", 20, settings.COLOR_ORANGE, topleft=(cx - 20, 120), bold=True)
            hud.draw_text(self.window, "DATA", 20, settings.COLOR_ORANGE, topleft=(cx + 100, 120), bold=True)
            if not rows:
                hud.draw_text(self.window, "Nenhuma pontuacao ainda. Jogue!", 22,
                              settings.COLOR_WHITE, center=(cx, 200))
            for i, (name, score, played_at) in enumerate(rows):
                hud.draw_text(self.window, name, 20, settings.COLOR_WHITE,
                              topleft=(cx - 200, 160 + i * 30))
                hud.draw_text(self.window, str(score), 20, settings.COLOR_WHITE,
                              topleft=(cx - 20, 160 + i * 30))
                hud.draw_text(self.window, played_at, 20, settings.COLOR_WHITE,
                              topleft=(cx + 100, 160 + i * 30))
            hud.draw_text(self.window, "Esc - Voltar ao menu", 18,
                          settings.COLOR_WHITE, center=(cx, settings.WIN_HEIGHT - 30))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
