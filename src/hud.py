#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Funcoes utilitarias de interface (texto e barra de vida).
"""
import pygame

from src import settings


def draw_text(surface, text, size, color, center=None, topleft=None, bold=False):
    font = pygame.font.SysFont("Verdana", size, bold=bold)
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    surface.blit(img, rect)
    return rect


def draw_health_bar(surface, x, y, value, maximum, width=180, height=14,
                    color=settings.COLOR_GREEN):
    value = max(0, value)
    ratio = value / maximum if maximum else 0
    pygame.draw.rect(surface, settings.COLOR_DARK, (x - 1, y - 1, width + 2, height + 2))
    pygame.draw.rect(surface, (70, 70, 80), (x, y, width, height))
    bar = color if ratio > 0.3 else settings.COLOR_RED
    pygame.draw.rect(surface, bar, (x, y, int(width * ratio), height))
