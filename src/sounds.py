#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Gerador de áudio sintético (retro chiptune) em tempo de execução.

Gera efeitos sonoros (SFX) e uma trilha sonora em loop (BGM) diretamente na
memória usando fórmulas matemáticas simples (ondas senoidais, quadradas e ruído),
criando objetos pygame.mixer.Sound sem precisar de arquivos de áudio externos.
"""
import math
import os
import random
import struct
import pygame

SOUNDS = {}
_bgm_channel = None
_bgm_sound = None
_enabled = False
_use_midi = False


def init_sounds():
    global _enabled, _bgm_sound, _use_midi
    if _enabled:
        return
    try:
        # Se o mixer não estiver inicializado, inicializa com 22.05kHz, 16-bit mono
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=1)

        SOUNDS["shoot"] = _make_shoot()
        SOUNDS["hit"] = _make_hit()
        SOUNDS["explosion"] = _make_explosion()
        SOUNDS["life_bonus"] = _make_life_bonus()
        SOUNDS["victory"] = _make_victory()
        SOUNDS["game_over"] = _make_game_over()

        # Verifica se o arquivo midi existe para usá-lo como BGM
        from src.assets import asset
        midi_path = asset("praia-de-janga.mid")
        if os.path.exists(midi_path):
            _use_midi = True
            pygame.mixer.music.load(midi_path)
        else:
            _bgm_sound = _make_bgm()

        _enabled = True
    except Exception as exc:
        print(f"[sounds] aviso: nao foi possivel inicializar mixer de audio ({exc})")
        _enabled = False


def play_sound(name):
    if not _enabled or name not in SOUNDS:
        return
    SOUNDS[name].play()


def start_bgm():
    global _bgm_channel
    if not _enabled:
        return
    if _use_midi:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.4)
    else:
        if _bgm_sound is None:
            return
        if _bgm_channel is None or not _bgm_channel.get_busy():
            _bgm_channel = _bgm_sound.play(loops=-1)
            if _bgm_channel:
                _bgm_channel.set_volume(0.4)


def stop_bgm():
    global _bgm_channel
    if not _enabled:
        return
    if _use_midi:
        pygame.mixer.music.stop()
    else:
        if _bgm_channel is not None:
            _bgm_channel.stop()



def play_victory():
    stop_bgm()
    play_sound("victory")


def play_game_over():
    stop_bgm()
    play_sound("game_over")


# --- Auxiliares de síntese ---------------------------------------------------

def _make_shoot():
    sr = 22050
    dur = 0.10
    buf = bytearray()
    for i in range(int(sr * dur)):
        t = i / sr
        freq = 900 - 800 * (t / dur)
        phase = 2 * math.pi * (900 * t - 400 * t * t / dur)
        val = int(math.sin(phase) * 12000)
        buf.extend(struct.pack("<h", val))
    return pygame.mixer.Sound(buffer=buf)


def _make_hit():
    sr = 22050
    dur = 0.08
    buf = bytearray()
    for i in range(int(sr * dur)):
        noise = random.randint(-16000, 16000)
        val = int(noise * (1.0 - i / (sr * dur)))
        buf.extend(struct.pack("<h", val))
    return pygame.mixer.Sound(buffer=buf)


def _make_explosion():
    sr = 22050
    dur = 0.35
    buf = bytearray()
    for i in range(int(sr * dur)):
        t = i / sr
        p = t / dur
        noise = random.randint(-24000, 24000)
        rumble = math.sin(2 * math.pi * (120 * t - 80 * t * t / dur)) * 16000
        val = int((noise * 0.4 + rumble * 0.6) * (1.0 - p))
        buf.extend(struct.pack("<h", val))
    return pygame.mixer.Sound(buffer=buf)


def _make_life_bonus():
    sr = 22050
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5 -> E5 -> G5 -> C6
    note_dur = 0.08
    buf = bytearray()
    for freq in notes:
        for i in range(int(sr * note_dur)):
            t = i / sr
            val = int(math.sin(2 * math.pi * freq * t) * 12000 * (1.0 - t / note_dur))
            buf.extend(struct.pack("<h", val))
    return pygame.mixer.Sound(buffer=buf)


def _make_victory():
    sr = 22050
    notes = [523.25, 783.99, 659.25, 1046.50]
    note_dur = 0.15
    buf = bytearray()
    for freq in notes:
        for i in range(int(sr * note_dur)):
            t = i / sr
            val = int(math.sin(2 * math.pi * freq * t) * 10000 * (1.0 - t / note_dur * 0.5))
            buf.extend(struct.pack("<h", val))
    return pygame.mixer.Sound(buffer=buf)


def _make_game_over():
    sr = 22050
    notes = [392.00, 329.63, 311.13, 261.63]  # G4 -> E4 -> Eb4 -> C4
    note_dur = 0.25
    buf = bytearray()
    for freq in notes:
        for i in range(int(sr * note_dur)):
            t = i / sr
            val = int(math.sin(2 * math.pi * freq * t) * 10000 * (1.0 - t / note_dur))
            buf.extend(struct.pack("<h", val))
    return pygame.mixer.Sound(buffer=buf)


def _make_bgm():
    sr = 22050
    # Progressão de acordes: Am (1s), G (1s), F (1s), E (1s)
    chords = [
        [220.00, 261.63, 329.63],
        [196.00, 246.94, 293.66],
        [174.61, 220.00, 261.63],
        [164.81, 207.65, 246.94],
    ]
    total_duration = 4.0
    num_samples = int(sr * total_duration)
    buf = bytearray()
    for i in range(num_samples):
        t = i / sr
        chord_idx = int(t / 1.0) % 4
        note_idx = int((t % 1.0) / 0.25)
        notes = chords[chord_idx]
        freq = notes[note_idx % len(notes)]

        # Onda triangular para melodia
        tf = t * freq
        val_tri = 4.0 * abs(tf - math.floor(tf + 0.5)) - 1.0

        # Baixo (onda quadrada uma oitava abaixo)
        bass_freq = notes[0] / 2
        tf_bass = t * bass_freq
        val_bass = 1.0 if (tf_bass - math.floor(tf_bass) < 0.5) else -1.0

        # Mixagem simples
        val = int((val_tri * 0.45 + val_bass * 0.35) * 6000)
        buf.extend(struct.pack("<h", val))

    return pygame.mixer.Sound(buffer=buf)
