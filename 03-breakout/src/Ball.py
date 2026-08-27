"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Ball.
"""

import random
from typing import Any, Tuple, Optional

import pygame

from gale.timer import Timer

import settings
from src.Paddle import Paddle


class Ball:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

        self.vx = 0
        self.vy = 0

        self.texture = settings.TEXTURES["spritesheet"]
        self.frame = random.randint(0, 6)
        self.active = True
        self.caught = False
        self.paddle = None
        self.catch_offset = 0

        self.alpha = 255
        self._blink_tween = None
        self._blink_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def solve_world_boundaries(self) -> None:
        r = self.get_collision_rect()

        if r.left < 0:
            settings.SOUNDS["wall_hit"].stop()
            settings.SOUNDS["wall_hit"].play()
            self.x = 0
            self.vx *= -1
        elif r.right > settings.VIRTUAL_WIDTH:
            settings.SOUNDS["wall_hit"].stop()
            settings.SOUNDS["wall_hit"].play()
            self.x = settings.VIRTUAL_WIDTH - self.width
            self.vx *= -1
        elif r.top < 0:
            settings.SOUNDS["wall_hit"].stop()
            settings.SOUNDS["wall_hit"].play()
            self.y = 0
            self.vy *= -1
        elif r.top > settings.VIRTUAL_HEIGHT:
            if not self.caught:
                settings.SOUNDS["hurt"].play()
                self.active = False

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def catch(self, paddle: Paddle) -> None:
        self.caught = True
        self.paddle = paddle
        self.catch_offset = self.x - paddle.x
        self.vx = 0
        self.vy = 0
        self.y = paddle.y - self.height

    def release(self) -> None:
        self.caught = False
        self.paddle = None
        self.vx = random.randint(-80, 80)
        self.vy = random.randint(-170, -100)

    def start_blink(self) -> None:
        if self._blink_tween is not None:
            return

        def fade_out():
            self._blink_tween = Timer.tween(
                0.3,
                [(self, {"alpha": 80})],
                ease_function_name="in_out_sine",
                on_finish=fade_in,
            )

        def fade_in():
            self._blink_tween = Timer.tween(
                0.3,
                [(self, {"alpha": 255})],
                ease_function_name="in_out_sine",
                on_finish=fade_out,
            )

        fade_in()

    def stop_blink(self) -> None:
        if self._blink_tween is not None:
            self._blink_tween.remove()
            self._blink_tween = None
        self.alpha = 255

    def update(self, dt: float) -> None:
        if self.caught and self.paddle is not None:
            self.x = self.paddle.x + self.catch_offset
            self.y = self.paddle.y - self.height
        else:
            self.x += self.vx * dt
            self.y += self.vy * dt

    def render(self, surface):
        if self.alpha < 255:
            self._blink_surface.fill((0, 0, 0, 0))
            self._blink_surface.blit(
                self.texture, (0, 0), settings.FRAMES["balls"][self.frame]
            )
            self._blink_surface.set_alpha(int(self.alpha))
            surface.blit(self._blink_surface, (self.x, self.y))
        else:
            surface.blit(
                self.texture, (self.x, self.y), settings.FRAMES["balls"][self.frame]
            )

    @staticmethod
    def get_intersection(r1: pygame.Rect, r2: pygame.Rect) -> Optional[Tuple[int, int]]:
        """
        Compute, if exists, the intersection between two
        rectangles.
        """
        if r1.x > r2.right or r1.right < r2.x or r1.bottom < r2.y or r1.y > r2.bottom:
            # There is no intersection
            return None

        # Compute x shift
        if r1.centerx < r2.centerx:
            x_shift = r2.x - r1.right
        else:
            x_shift = r2.right - r1.x

        # Compute y shift
        if r1.centery < r2.centery:
            y_shift = r2.y - r1.bottom
        else:
            y_shift = r2.bottom - r1.y

        return (x_shift, y_shift)

    def rebound(self, another: Any):
        br = self.get_collision_rect()
        sr = another.get_collision_rect()

        r = self.get_intersection(br, sr)

        if r is None:
            return

        shift_x, shift_y = r

        min_shift = min(abs(shift_x), abs(shift_y))

        if min_shift == abs(shift_x):
            # Collision happened from left or right
            self.x += shift_x
            self.vx *= -1
        else:
            # Collision happened from top or bottom
            self.y += shift_y
            self.vy *= -1

    def push(self, paddle: Paddle) -> None:
        """
        Push the ball according to the position that it collides with the paddle and the paddle speed.
        """
        br = self.get_collision_rect()
        pr = paddle.get_collision_rect()
        d = pr.centerx - br.x

        if d > 0 and paddle.vx < 0 and pr.x > 0:
            self.vx = -50 - 8 * d
        elif d < 0 and paddle.vx > 0 and pr.right < settings.VIRTUAL_HEIGHT:
            self.vx = 50 - 8 * d
