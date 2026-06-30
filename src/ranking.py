#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Ranking de pontuacoes com persistencia em SQLite (padrao Proxy).

A classe ScoreDB encapsula o acesso ao banco: cria a tabela, salva uma
nova pontuacao e recupera o Top N. O restante do jogo nao conhece SQL.
"""
import os
import sqlite3
from datetime import datetime

from src import settings
from src.assets import base_path


class ScoreDB:
    def __init__(self):
        # grava o banco ao lado do executavel/projeto
        self.path = os.path.join(base_path(), settings.DB_NAME)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS ranking (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   score INTEGER NOT NULL,
                   played_at TEXT NOT NULL)"""
        )
        self.conn.commit()

    def save(self, name, score):
        moment = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.conn.execute(
            "INSERT INTO ranking (name, score, played_at) VALUES (?, ?, ?)",
            (name, score, moment),
        )
        self.conn.commit()

    def top(self, limit=settings.RANKING_LIMIT):
        cur = self.conn.execute(
            "SELECT name, score, played_at FROM ranking ORDER BY score DESC LIMIT ?",
            (limit,),
        )
        return cur.fetchall()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

