#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Arbitro de interacoes (padrao Mediator).

Concentra a logica de colisao e de remocao de entidades mortas, evitando
que cada classe conheca as outras. Trata:
  - tiro do heroi atingindo monstros/chefe;
  - tiros inimigos atingindo o heroi;
  - contato direto monstro x heroi;
  - pontuacao concedida ao heroi quando um inimigo morre.
"""
from src import settings
from src.boss import Boss
from src.bullet import HeroBullet, MonsterBullet
from src.hero import Hero
from src.monster import Monster


class Arbiter:
    @staticmethod
    def _hit(a, b):
        a.health -= b.damage
        b.health -= a.damage
        a.last_hit_by = b.name
        b.last_hit_by = a.name

    @staticmethod
    def resolve_collisions(entities, hero):
        enemies = [e for e in entities if isinstance(e, (Monster, Boss))]
        hero_bullets = [e for e in entities if isinstance(e, HeroBullet)]
        enemy_bullets = [e for e in entities if isinstance(e, MonsterBullet)]

        # tiros do heroi x inimigos
        for bullet in hero_bullets:
            for enemy in enemies:
                if bullet.is_alive and enemy.collides_with(bullet):
                    Arbiter._hit(enemy, bullet)

        # tiros inimigos x heroi
        for bullet in enemy_bullets:
            if hero.is_alive and not hero.is_invincible and hero.collides_with(bullet):
                Arbiter._hit(hero, bullet)
                hero.invincible_timer = settings.INVINCIBILITY_FRAMES

        # contato direto monstro x heroi
        for enemy in enemies:
            if hero.is_alive and not hero.is_invincible and hero.collides_with(enemy):
                Arbiter._hit(hero, enemy)
                hero.invincible_timer = settings.INVINCIBILITY_FRAMES


    @staticmethod
    def collect_dead(entities, hero):
        """Remove entidades sem vida e devolve a pontuacao conquistada."""
        gained = 0
        survivors = []
        for ent in entities:
            if ent.is_alive or ent is hero:
                survivors.append(ent)
            else:
                if isinstance(ent, (Monster, Boss)) and ent.last_hit_by == hero.name + "_bullet":
                    gained += ent.score
        entities[:] = survivors
        return gained
