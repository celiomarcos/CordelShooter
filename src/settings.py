#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Configuracoes globais do Cordel Shooter.

Centraliza dimensoes da janela, cores, eventos customizados e os
atributos de cada entidade (velocidade, vida, dano, pontuacao e
cadencia de tiro). Manter esses valores em um unico lugar facilita o
balanceamento do jogo sem mexer na logica.
"""
import pygame

# ----------------------------------------------------------------------
# Janela
# ----------------------------------------------------------------------
WIN_WIDTH = 800
WIN_HEIGHT = 600
GAME_TITLE = "Cordel Shooter - Lendas do Sertao"
FPS = 60

# ----------------------------------------------------------------------
# Cores
# ----------------------------------------------------------------------
COLOR_WHITE = (240, 240, 230)
COLOR_YELLOW = (250, 214, 96)
COLOR_ORANGE = (232, 120, 52)
COLOR_RED = (208, 56, 56)
COLOR_GREEN = (110, 200, 90)
COLOR_BLUE = (120, 170, 240)
COLOR_PURPLE = (170, 110, 220)
COLOR_DARK = (24, 20, 48)

# ----------------------------------------------------------------------
# Eventos customizados
# ----------------------------------------------------------------------
EVENT_SPAWN = pygame.USEREVENT + 1     # gerar novo monstro
EVENT_CLOCK = pygame.USEREVENT + 2     # passo do cronometro

CLOCK_STEP_MS = 100                     # cada passo do cronometro = 100ms
WAVE_DURATION_MS = 35000                # duracao da horda antes do chefe (35s)
SPAWN_INTERVAL_MS = 1300                # intervalo entre monstros

# ----------------------------------------------------------------------
# Identificadores de entidades
# ----------------------------------------------------------------------
HERO = "hero"
HERO_BULLET = "hero_bullet"
MONSTER_BULLET = "monster_bullet"
BOSS_BULLET = "boss_bullet"
BOSS = "cuca"
MONSTERS = ("saci", "mula", "boitata")
BACKGROUNDS = ("bg_sky", "bg_caatinga")

# ----------------------------------------------------------------------
# Atributos das entidades
# ----------------------------------------------------------------------
SPEED = {
    "hero": 5,
    "hero_bullet": 9,
    "saci": 2,
    "mula": 3,
    "boitata": 2,
    "cuca": 2,
    "monster_bullet": 5,
    "boss_bullet": 4,
    "bg_sky": 0,
    "bg_caatinga": 1,
}

HEALTH = {
    "hero": 120,
    "hero_bullet": 1,
    "saci": 30,
    "mula": 50,
    "boitata": 40,
    "cuca": 600,
    "monster_bullet": 1,
    "boss_bullet": 1,
}

DAMAGE = {
    "hero": 10,
    "hero_bullet": 20,
    "saci": 10,
    "mula": 15,
    "boitata": 12,
    "cuca": 30,
    "monster_bullet": 12,
    "boss_bullet": 22,
}

SCORE_VALUE = {
    "saci": 100,
    "mula": 150,
    "boitata": 120,
    "cuca": 1000,
}

# cadencia de tiro (em frames; quanto menor, mais rapido)
SHOOT_COOLDOWN = {
    "hero": 12,
    "saci": 90,
    "mula": 70,
    "boitata": 80,
    "cuca": 35,
}

# ----------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------
MENU_NEW_GAME = "JOGAR"
MENU_RANKING = "RANKING"
MENU_EXIT = "SAIR"
MENU_OPTIONS = (MENU_NEW_GAME, MENU_RANKING, MENU_EXIT)

# Texto de controles exibido no menu (exigencia da atividade)
CONTROLS_TEXT = (
    "Setas / WASD - Mover",
    "Espaco - Atirar",
    "Enter - Confirmar    Esc - Voltar/Sair",
)

# ----------------------------------------------------------------------
# Condicoes de vitoria / derrota
# ----------------------------------------------------------------------
# Vitoria: derrotar a Cuca (chefe). Derrota: vida do heroi chega a zero.
VICTORY_MESSAGE = "VOCE VENCEU!"
DEFEAT_MESSAGE = "VOCE PERDEU!"

DB_NAME = "ranking.db"
RANKING_LIMIT = 10
