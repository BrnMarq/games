"""
ISPPV1-I2026
Study Case: Super Martian (Platformer)

Author: Brian Marquez
brnmarq@gmail.com

This file contains the CollidableMixin.
"""

from typing import Any

import pygame


class CollidableMixin:
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())
