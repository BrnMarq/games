"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Bird.
"""

import pygame

from gale.timer import Timer

import settings


class Bird:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.vx: float = 0.0
        self.jumping: bool = False

        self.ghost_time_left = 0
        self.ghost_alpha: float = 0
        self.ghost_overlay = settings.TEXTURES["bird"].copy()
        self.ghost_overlay.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
        self._ghost_tween = None

    def start_ghost_pulse(self) -> None:
        def fade_out():
            self._ghost_tween = Timer.tween(
                0.4,
                [(self, {"ghost_alpha": 0})],
                ease_function_name="in_out_sine",
                on_finish=fade_in,
            )

        def fade_in():
            self._ghost_tween = Timer.tween(
                0.4,
                [(self, {"ghost_alpha": 180})],
                ease_function_name="in_out_sine",
                on_finish=fade_out,
            )

        fade_in()

    def stop_ghost_pulse(self) -> None:
        if self._ghost_tween is not None:
            self._ghost_tween.remove()
            self._ghost_tween = None
        self.ghost_alpha = 0

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def jump(self) -> None:
        self.jumping = True

    def update(self, dt: float) -> None:
        self.vy += settings.GRAVITY * dt
        if self.jumping:
            settings.SOUNDS["jump"].play()
            self.vy = -settings.JUMP_TAKEOFF_SPEED
            self.jumping = False

        if self.ghost_time_left > 0:
            self.ghost_time_left -= dt
            if self.ghost_time_left <= 0:
                self.stop_ghost_pulse()

        self.y += self.vy * dt
        self.y = max(self.y, 0)
        self.x += self.vx * dt
        self.x = max(0, min(settings.VIRTUAL_WIDTH - settings.BIRD_WIDTH, self.x))

    def render(self, surface: pygame.Surface) -> None:
        bird_rect = self.get_rect()
        surface.blit(settings.TEXTURES["bird"], bird_rect)
        if self.ghost_time_left > 0:
            self.ghost_overlay.set_alpha(int(self.ghost_alpha))
            surface.blit(self.ghost_overlay, bird_rect)
