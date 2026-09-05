"""
ISPPV1-I2026
Study Case: Flappy Bird

Author: Brian Marquez
brnmarq@gmail.com

This file contains the game settings that include the association of the
inputs with an their ids, constants of values to set up the game, sounds,
textures, and fonts.
"""

from pathlib import Path

import pygame

from gale import input_handler

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_BACKSPACE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "pause")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "confirm")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_h, "secondary_option")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_n, "primary_option")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "jump")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_w, "jump")
input_handler.InputHandler.set_mouse_click_action(input_handler.MOUSE_BUTTON_1, "jump")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_a, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_d, "move_right")

TITLE = "Flappy Bird"

# Size of our actual window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Size we are trying to emulate
VIRTUAL_WIDTH = 512
VIRTUAL_HEIGHT = 288

BIRD_WIDTH = 39
BIRD_HEIGHT = 28
BIRD_X_SPEED = 100

LOG_WIDTH = 70
LOG_HEIGHT = 288
LOGS_GAP = 90
LOG_CLOSE_SPEED = 50
CLOSING_LOGS_CHANCE = 30  # 30%

GROUND_HEIGHT = 16

BACKGROUND_LOOPING_POINT = 1157

MAIN_SCROLL_SPEED = 100
BACK_SCROLL_SPEED = 50  # MAIN_SCROLL_SPEED / 2

GRAVITY = 980
JUMP_TAKEOFF_SPEED = GRAVITY / 6

TIME_TO_SPAWN_LOGS = 1.5

STAR_SIZE = 25
STAR_SPAWN_CHANCE = 5
GHOST_DURATION = 10

MEDIUM_TEXT_SIZE = 18
HUGE_TEXT_SIZE = 56
FLAPPY_TEXT_SIZE = 28

BASE_DIR = Path(__file__).parent

TEXTURES = {
    "bird": pygame.image.load(BASE_DIR / "assets" / "graphics" / "bird.png"),
    "background": pygame.image.load(
        BASE_DIR / "assets" / "graphics" / "background.png"
    ),
    "ground": pygame.image.load(BASE_DIR / "assets" / "graphics" / "ground.png"),
    "log": pygame.image.load(BASE_DIR / "assets" / "graphics" / "log.png"),
    "star": pygame.image.load(BASE_DIR / "assets" / "graphics" / "star.png"),
}
# The top log of every pair is the same image, flipped upside down.
TEXTURES["log_inverted"] = pygame.transform.flip(TEXTURES["log"], False, True)

SOUNDS = {
    "jump": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "jump.wav"),
    "explosion": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "explosion.wav"),
    "hurt": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "hurt.wav"),
    "score": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "score.wav"),
    "wood_crush": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "wood_crush.ogg"),
}

pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "marios_way.ogg")

GHOST_MUSIC_PATH = BASE_DIR / "assets" / "sounds" / "ttfaf.ogg"
NORMAL_MUSIC_PATH = BASE_DIR / "assets" / "sounds" / "marios_way.ogg"

FONTS = {
    "medium": pygame.font.Font(
        BASE_DIR / "assets" / "fonts" / "font.ttf", MEDIUM_TEXT_SIZE
    ),
    "huge": pygame.font.Font(
        BASE_DIR / "assets" / "fonts" / "font.ttf", HUGE_TEXT_SIZE
    ),
    "flappy": pygame.font.Font(
        BASE_DIR / "assets" / "fonts" / "flappy.ttf", FLAPPY_TEXT_SIZE
    ),
}

COLOR_BACKGROUND = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
