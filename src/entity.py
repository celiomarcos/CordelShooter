#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Classe base abstrata de todas as entidades do jogo.

Aplica o conceito de heranca: heroi, monstros, tiros, chefe e cenario
sao especializacoes de Entity. Cada entidade carrega sua imagem, posicao
(rect) e atributos numericos lidos de settings. O metodo update() e
abstrato e deve ser implementado por cada subclasse.
"""
from abc import ABC, abstractmethod

from src import settings
from src.assets import load_image


class Entity(ABC):
    def __init__(self, name, position):
        self.name = name
        self.surf = load_image(f"{name}.png")
        self.rect = self.surf.get_rect()
        self.rect.center = position
        self.speed = settings.SPEED.get(name, 0)
        self.health = settings.HEALTH.get(name, 1)
        self.max_health = self.health
        self.damage = settings.DAMAGE.get(name, 0)
        self.score = settings.SCORE_VALUE.get(name, 0)
        self.last_hit_by = None

    @property
    def is_alive(self):
        return self.health > 0

    @property
    def hitbox(self):
        """Caixa de colisao reduzida, focada no desenho (ignora a borda
        transparente do sprite). A reducao por entidade vem de settings."""
        shrink = settings.HITBOX_SHRINK.get(self.name, settings.HITBOX_SHRINK_DEFAULT)
        return self.rect.inflate(-int(self.rect.width * shrink),
                                 -int(self.rect.height * shrink))

    def collides_with(self, other):
        return self.hitbox.colliderect(other.hitbox)

    @abstractmethod
    def update(self):
        """Atualiza a posicao/estado da entidade a cada frame."""
        raise NotImplementedError
