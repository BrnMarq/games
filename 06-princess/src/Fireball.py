"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class Fireball — an enemy projectile that travels
in a straight line toward the player's position at the time of firing.
Rendered as a colored rectangle until a dedicated sprite is provided.
"""

import math

import pygame

import settings

_FIREBALL_SPEED = 120
_FIREBALL_SIZE = 8
_FIREBALL_COLOR = (255, 80, 20)  # Orange-red


class Fireball:
    def __init__(
        self, x: float, y: float, target_x: float, target_y: float
    ) -> None:
        self.x = x
        self.y = y
        self.width = _FIREBALL_SIZE
        self.height = _FIREBALL_SIZE
        self.dead = False

        # Calculate velocity toward target.
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            self.vx = dx / dist * _FIREBALL_SPEED
            self.vy = dy / dist * _FIREBALL_SPEED
        else:
            # Fallback: fire downward if the boss is exactly on the player.
            self.vx = 0
            self.vy = _FIREBALL_SPEED

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        if self.dead:
            return

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Die when hitting room boundaries.
        left = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE
        right = settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2
        top = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE
        bottom = (
            settings.MAP_HEIGHT * settings.TILE_SIZE
            + settings.MAP_RENDER_OFFSET_Y
            - settings.TILE_SIZE
        )

        if (
            self.x <= left
            or self.x + self.width >= right
            or self.y <= top
            or self.y + self.height >= bottom
        ):
            self.dead = True

    def render(
        self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0
    ) -> None:
        pygame.draw.rect(
            surface,
            _FIREBALL_COLOR,
            pygame.Rect(
                round(self.x + offset_x),
                round(self.y + offset_y),
                self.width,
                self.height,
            ),
        )

    def collides(self, target) -> bool:
        return self.get_collision_rect().colliderect(target.get_collision_rect())
