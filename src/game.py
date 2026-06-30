#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Maquina de estados principal do jogo.

Liga menu -> fase -> tela de fim -> ranking, repetindo ate o jogador
sair. Em caso de vitoria, pede um nome e grava a pontuacao no ranking.
"""
import sys

import pygame

from src import hud, settings, sounds
from src.assets import ensure_assets
from src.menu import Menu
from src.ranking import ScoreDB
from src.world import World


class Game:
    def __init__(self):
        pygame.init()
        # garante que todos os assets existam antes de carregar imagens
        ensure_assets(settings.WIN_WIDTH, settings.WIN_HEIGHT)
        sounds.init_sounds()
        self.window = pygame.display.set_mode((settings.WIN_WIDTH, settings.WIN_HEIGHT))
        pygame.display.set_caption(settings.GAME_TITLE)
        self.menu = Menu(self.window)


    def run(self):
        while True:
            choice = self.menu.run()
            if choice == settings.MENU_NEW_GAME:
                self._play_session()
            elif choice == settings.MENU_RANKING:
                self.menu.show_ranking()
            elif choice == settings.MENU_EXIT:
                pygame.quit()
                sys.exit()

    # ------------------------------------------------------------------
    def _play_session(self):
        world = World(self.window)
        result, score = world.run()
        if result == "quit":
            sounds.stop_bgm()
            return
        if result == "win":
            sounds.play_victory()
            self._end_screen(settings.VICTORY_MESSAGE, settings.COLOR_YELLOW, score)
            name = self._ask_name()
            if name:
                with ScoreDB() as db:
                    db.save(name, score)

        else:  # lose
            sounds.play_game_over()
            self._end_screen(settings.DEFEAT_MESSAGE, settings.COLOR_RED, score)


    def _end_screen(self, message, color, score):
        clock = pygame.time.Clock()
        while True:
            clock.tick(settings.FPS)
            self.window.fill(settings.COLOR_DARK)
            cx = settings.WIN_WIDTH // 2
            hud.draw_text(self.window, message, 64, color,
                          center=(cx, settings.WIN_HEIGHT // 2 - 60), bold=True)
            hud.draw_text(self.window, f"Pontuacao: {score}", 30, settings.COLOR_WHITE,
                          center=(cx, settings.WIN_HEIGHT // 2 + 10))
            hud.draw_text(self.window, "Enter - Continuar", 22, settings.COLOR_WHITE,
                          center=(cx, settings.WIN_HEIGHT // 2 + 70))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return

    def _ask_name(self):
        """Tela de entrada de nome (ate 8 caracteres) para o ranking."""
        name = ""
        clock = pygame.time.Clock()
        while True:
            clock.tick(settings.FPS)
            self.window.fill(settings.COLOR_DARK)
            cx = settings.WIN_WIDTH // 2
            hud.draw_text(self.window, "Digite seu nome:", 30, settings.COLOR_YELLOW,
                          center=(cx, 220))
            hud.draw_text(self.window, name + "_", 36, settings.COLOR_WHITE,
                          center=(cx, 280))
            hud.draw_text(self.window, "Enter - Salvar    Esc - Pular", 20,
                          settings.COLOR_WHITE, center=(cx, 360))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        return name
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.unicode.isalnum() and len(name) < 8:
                        name += event.unicode.upper()
