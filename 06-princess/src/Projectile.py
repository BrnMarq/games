"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Projectile.
"""

from typing import Any

import pygame

import settings

_SPEED = 150
_MAX_TILES = 4


class Projectile:
    def __init__(self, obj: Any, direction: str) -> None:
        self.obj = obj
        self.direction = direction
        self.distance = 0.0
        self.dead = False

    def get_collision_rect(self) -> pygame.Rect:
        return self.obj.get_collision_rect()

    def update(self, dt: float) -> None:
        if self.dead:
            return

        d = _SPEED * dt

        if self.direction == "up":
            self.obj.y -= d
            limit = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE - self.obj.height / 2
            if self.obj.y <= limit:
                self.obj.y = limit
                self.dead = True
        elif self.direction == "down":
            self.obj.y += d
            bottom_edge = (
                settings.MAP_HEIGHT * settings.TILE_SIZE
                + settings.MAP_RENDER_OFFSET_Y
                - settings.TILE_SIZE
            )
            if self.obj.y + self.obj.height >= bottom_edge:
                self.obj.y = bottom_edge - self.obj.height
                self.dead = True
        elif self.direction == "left":
            self.obj.x -= d
            limit = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE
            if self.obj.x <= limit:
                self.obj.x = limit
                self.dead = True
        elif self.direction == "right":
            self.obj.x += d
            limit = settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2
            if self.obj.x + self.obj.width >= limit:
                self.obj.x = limit - self.obj.width
                self.dead = True

        if self.dead:
            settings.SOUNDS["pot-wall"].play()
            return

        self.distance += d

        if self.distance > _MAX_TILES * settings.TILE_SIZE:
            self.dead = True

    def render(
        self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0
    ) -> None:
        _DIRECTION_ANGLES = {"up": 0, "down": 180, "left": 90, "right": -90}
        angle = _DIRECTION_ANGLES.get(self.direction)

        if angle is None or angle == 0:
            # No rotation needed — delegate normally.
            self.obj.render(surface, offset_x, offset_y)
            return

        # Grab the sub-surface for the current frame, rotate it, then blit.
        frame_rect = settings.frame(self.obj.texture_id, self.obj.states[self.obj.state].get("frame", self.obj.frame_index))
        sprite = settings.TEXTURES[self.obj.texture_id].subsurface(frame_rect)
        rotated = pygame.transform.rotate(sprite, angle)
        surface.blit(rotated, (self.obj.x + offset_x, self.obj.y + offset_y))

    def collides(self, target: Any) -> bool:
        return self.get_collision_rect().colliderect(target.get_collision_rect())
