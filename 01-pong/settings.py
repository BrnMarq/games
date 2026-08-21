from pathlib import Path

import pygame

from gale import input_handler

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "confirm")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_w, "p1_up")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_s, "p1_down")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "p2_up")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "p2_down")

TITLE = "Pong"

# Size of our actual window. The original creates a plain 320x200
# window with no virtual-resolution scaling, so window and virtual
# sizes match here too.
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Size we are trying to emulate
VIRTUAL_WIDTH = 432
VIRTUAL_HEIGHT = 243

# Game Configs
PADDLE_WIDTH = 5
PADDLE_HEIGHT = 20
PADDLE_X_OFFSET = 10
PADDLE_Y_OFFSET = 30
PADDLE_SPEED = 200

BALL_SIZE = 4

MID_LINE_WIDTH = 2

MAX_POINTS = 5

BASE_DIR = Path(__file__).parent

SOUNDS = {
    "paddle_hit": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "paddle_hit.wav"),
    "wall_hit": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "wall_hit.wav"),
    "score": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "score.wav"),
}

FONTS = {
    "score": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 32),
    "large": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
}

COLOR_BACKGROUND = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
