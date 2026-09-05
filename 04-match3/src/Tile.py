"""
ISPPV1-I2026
Study Case: Match-3

Author: Brian Marquez
brnmarq@gmail.com

This file contains the class Tile.
"""

import pygame

import settings


class Tile:
    def __init__(self, i: int, j: int, color: int, variety: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.color = color
        self.powerup = None
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        if self.powerup == "line_clear":
            frame = settings.LINE_CLEAR_TILE_FRAME
        elif self.powerup == "bomb":
            frame = settings.BOMB_TILE_FRAME
        else:
            frame = settings.BASE_TILE_FRAME
        self.alpha_surface.blit(
            settings.TEXTURES["tiles"],
            (0, 0),
            settings.FRAMES["tiles"][self.color][frame],
        )
        pygame.draw.rect(
            self.alpha_surface,
            (34, 32, 52, 200),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )
        surface.blit(self.alpha_surface, (self.x + 2 + offset_x, self.y + 2 + offset_y))
        surface.blit(
            settings.TEXTURES["tiles"],
            (self.x + offset_x, self.y + offset_y),
            settings.FRAMES["tiles"][self.color][frame],
        )
