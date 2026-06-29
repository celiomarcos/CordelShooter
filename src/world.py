#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Fase jogavel do Cordel Shooter.

Fluxo: o jogador enfrenta uma horda de monstros do folclore por um
tempo determinado; quando o cronometro zera, surge a Cuca (chefe).
  - Condicao de VITORIA: derrotar a Cuca.
  - Condicao de DERROTA: a vida do heroi chegar a zero.

run() devolve uma tupla (resultado, pontuacao), onde resultado e um de
'win', 'lose' ou 'quit'.
"""
import sys

import pygame

from src import hud, settings
from src.arbiter import Arbiter
from src.boss import Boss
from src.cheats import CHEATS
from src.hero import Hero
from src.monster import Monster
from src.spawner import Spawner


class World:
    def __init__(self, window):
        self.window = window
        self.background = Spawner.background()
        self.hero = Spawner.hero()
        if CHEATS.cangaco:  # easter egg: Modo Cangaco
            self.hero.cangaco = True
            self.hero.health = 200
            self.hero.max_health = 200
        self.entities = [self.hero]
        self.score = 0
        self.time_left = settings.WAVE_DURATION_MS
        self.boss = None
        self.boss_phase = False

    # ------------------------------------------------------------------
    def run(self):
        clock = pygame.time.Clock()
        pygame.time.set_timer(settings.EVENT_SPAWN, settings.SPAWN_INTERVAL_MS)
        pygame.time.set_timer(settings.EVENT_CLOCK, settings.CLOCK_STEP_MS)

        while True:
            clock.tick(settings.FPS)

            result = self._handle_events()
            if result is not None:
                self._stop_timers()
                return result, self.score

            self._update()
            self._draw(clock)

            # condicoes de fim de jogo
            if not self.hero.is_alive:
                self._stop_timers()
                return "lose", self.score
            # a pontuacao do chefe ja e concedida em Arbiter.collect_dead
            if self.boss_phase and self.boss is not None and not self.boss.is_alive:
                self._stop_timers()
                return "win", self.score

    # ------------------------------------------------------------------
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            if event.type == settings.EVENT_SPAWN and not self.boss_phase:
                self.entities.append(Spawner.random_monster())
            if event.type == settings.EVENT_CLOCK and not self.boss_phase:
                self.time_left -= settings.CLOCK_STEP_MS
                if self.time_left <= 0:
                    self._start_boss()
        return None

    def _start_boss(self):
        self.boss_phase = True
        self.time_left = 0
        pygame.time.set_timer(settings.EVENT_SPAWN, 0)  # para de gerar monstros
        self.boss = Spawner.boss()
        self.entities.append(self.boss)

    def _update(self):
        # cenario
        for layer in self.background:
            layer.update()

        # heroi e seu(s) tiro(s)
        self.hero.update()
        for shot in self.hero.try_shoot():
            self.entities.append(shot)

        # demais entidades (snapshot: novos tiros nao sao iterados neste frame)
        for ent in list(self.entities):
            if ent is self.hero:
                continue
            ent.update()
            if isinstance(ent, (Monster, Boss)):
                for enemy_shot in ent.try_shoot(self.hero):
                    self.entities.append(enemy_shot)

        # colisoes e limpeza
        Arbiter.resolve_collisions(self.entities, self.hero)
        self.score += Arbiter.collect_dead(self.entities, self.hero)

    # ------------------------------------------------------------------
    def _draw(self, clock):
        for layer in self.background:
            self.window.blit(layer.surf, layer.rect)
        for ent in self.entities:
            self.window.blit(ent.surf, ent.rect)
        self._draw_hud(clock)
        pygame.display.flip()

    def _draw_hud(self, clock):
        # vida do heroi
        hud.draw_text(self.window, "VIDA", 16, settings.COLOR_WHITE, topleft=(10, 8))
        hud.draw_health_bar(self.window, 60, 10, self.hero.health, self.hero.max_health)
        if self.hero.cangaco:  # indicador do easter egg
            hud.draw_text(self.window, "CANGACO", 13, settings.COLOR_YELLOW,
                          topleft=(60, 28), bold=True)
        # pontuacao
        hud.draw_text(self.window, f"PONTOS: {self.score}", 20, settings.COLOR_YELLOW,
                      topleft=(settings.WIN_WIDTH - 220, 8), bold=True)
        # cronometro ou aviso do chefe
        if self.boss_phase:
            hud.draw_text(self.window, "CHEFE: A CUCA!", 22, settings.COLOR_RED,
                          center=(settings.WIN_WIDTH // 2, 22), bold=True)
            if self.boss is not None and self.boss.is_alive:
                hud.draw_health_bar(self.window, settings.WIN_WIDTH // 2 - 150, 40,
                                    self.boss.health, self.boss.max_health,
                                    width=300, height=12, color=settings.COLOR_PURPLE)
        else:
            hud.draw_text(self.window, f"Horda: {self.time_left / 1000:.1f}s", 20,
                          settings.COLOR_WHITE, center=(settings.WIN_WIDTH // 2, 18))

    @staticmethod
    def _stop_timers():
        pygame.time.set_timer(settings.EVENT_SPAWN, 0)
        pygame.time.set_timer(settings.EVENT_CLOCK, 0)
