import pygame

from gale import input_handler

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")

TITLE = "Hello World"

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 200

VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 200

FONTS = {"default": pygame.font.Font(None, 16)}
