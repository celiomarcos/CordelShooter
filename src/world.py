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

from src import hud, settings, sounds
from src.arbiter import Arbiter
from src.boss import Boss
from src.bullet import HeroBullet
from src.cheats import CHEATS
from src.hero import Hero
from src.monster import Monster
from src.spawner import Spawner
from src.specials import ET, LifeBonus


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
        self.et = None              # ET de Varginha ativo (ou None)
        self._et_cooldown = 0       # espera entre aparicoes do ET
        self._msg = ""              # mensagem temporaria no HUD
        self._msg_timer = 0

    # ------------------------------------------------------------------
    def run(self):
        sounds.start_bgm()
        clock = pygame.time.Clock()

        pygame.time.set_timer(settings.EVENT_SPAWN, settings.SPAWN_INTERVAL_MS)
        pygame.time.set_timer(settings.EVENT_CLOCK, settings.CLOCK_STEP_MS)

        while True:
            dt = clock.tick(settings.FPS)
            dt_scale = min(dt / 1000.0, 0.1) * 60.0

            result = self._handle_events()
            if result is not None:
                self._stop_timers()
                return result, self.score

            self._update(dt_scale)
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

    def _update(self, dt_scale=1.0):
        # cenario
        for layer in self.background:
            layer.update(dt_scale)

        # heroi e seu(s) tiro(s)
        self.hero.update(dt_scale)
        for shot in self.hero.try_shoot():
            self.entities.append(shot)

        # demais entidades (snapshot: novos tiros nao sao iterados neste frame)
        for ent in list(self.entities):
            if ent is self.hero:
                continue
            ent.update(dt_scale)
            if isinstance(ent, (Monster, Boss)):
                for enemy_shot in ent.try_shoot(self.hero):
                    self.entities.append(enemy_shot)

        # ET de Varginha (socorro quando a vida esta baixa)
        self._update_et(dt_scale)

        # colisoes e limpeza
        Arbiter.resolve_collisions(self.entities, self.hero)
        self._handle_specials()
        self.score += Arbiter.collect_dead(self.entities, self.hero)

    # ------------------------------------------------------------------
    def _update_et(self, dt_scale=1.0):
        """Faz o ET aparecer quando o heroi esta com pouca vida."""
        if self._et_cooldown > 0:
            self._et_cooldown = max(0.0, self._et_cooldown - dt_scale)
        low = self.hero.health < self.hero.max_health * settings.ET_LOW_HEALTH_RATIO
        if self.et is None and self._et_cooldown <= 0 and low and self.hero.is_alive:
            self.et = Spawner.et()
            self.entities.append(self.et)
            self._et_cooldown = settings.ET_RESPAWN_FRAMES
            self._set_msg("apareceu o ET de Varginha! Acerte-o para ganhar vida!", 120)


    def _handle_specials(self):
        """Resolve tiros no ET (solta coracao) e a coleta do coracao."""
        # ET atingido pelos tiros do heroi
        if self.et is not None and self.et.is_alive:
            for bullet in self.entities:
                if isinstance(bullet, HeroBullet) and bullet.is_alive \
                        and self.et.collides_with(bullet):
                    self.et.health -= bullet.damage
                    bullet.health = 0
            if not self.et.is_alive:  # derrubado: solta o coracao
                self.entities.append(LifeBonus(self.et.rect.center))
                self._set_msg("Bonus de vida liberado!", 120)
        if self.et is not None and not self.et.is_alive:
            self.et = None

        # coleta do coracao pelo heroi
        for ent in self.entities:
            if isinstance(ent, LifeBonus) and ent.is_alive and self.hero.collides_with(ent):
                self.hero.health = min(self.hero.max_health,
                                       self.hero.health + settings.LIFE_BONUS_HEAL)
                ent.health = 0
                sounds.play_sound("life_bonus")
                self._set_msg(f"+{settings.LIFE_BONUS_HEAL} DE VIDA!", 90)


    def _set_msg(self, text, frames):
        self._msg = text
        self._msg_timer = frames

    def _draw(self, clock):
        for layer in self.background:
            self.window.blit(layer.surf, layer.rect)
        for ent in self.entities:
            if ent is self.hero and self.hero.is_invincible:
                if (self.hero.invincible_timer // 6) % 2 == 0:
                    self.window.blit(ent.surf, ent.rect)
            else:
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

        # mensagem temporaria (ET / bonus de vida)
        if self._msg_timer > 0:
            hud.draw_text(self.window, self._msg, 20, settings.COLOR_GREEN,
                          center=(settings.WIN_WIDTH // 2, settings.WIN_HEIGHT - 40),
                          bold=True)
            self._msg_timer -= 1

    @staticmethod
    def _stop_timers():
        pygame.time.set_timer(settings.EVENT_SPAWN, 0)
        pygame.time.set_timer(settings.EVENT_CLOCK, 0)
