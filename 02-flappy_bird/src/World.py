"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, and the log pairs the bird must fly through.
"""

import random
from typing import List

import pygame

from gale.factory import Factory

import settings
from src.LogPair import LogPair
from src.powerups import Star


class World:
    def __init__(self) -> None:
        self.background_x: float = 0.0
        self.ground_x: float = 0.0
        self.logs: List[LogPair] = []
        self.stars: List[Star] = []

    def collides_with_ground(self, rect: pygame.Rect):
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True

    def collides_with_logs(self, rect: pygame.Rect):
        return any(log_pair.collides(rect) for log_pair in self.logs)

    def collect_star(self, rect: pygame.Rect) -> Star | None:
        for star in self.stars:
            if star.get_rect().colliderect(rect):
                self.stars.remove(star)
                return star
        return None

    def collides(self, rect: pygame.Rect) -> bool:
        return self.collides_with_ground(rect) or self.collides_with_logs(rect)

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)

    def update(self, dt: float) -> None:
        self.background_x += -settings.BACK_SCROLL_SPEED * dt

        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0

        self.ground_x += -settings.MAIN_SCROLL_SPEED * dt

        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0

        for log_pair in self.logs:
            log_pair.update(dt)

        self.logs = [
            log_pair for log_pair in self.logs if not log_pair.is_out_of_game()
        ]

        for star in self.stars:
            star.update(dt)

        self.stars = [star for star in self.stars if not star.is_out_of_game()]

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for log_pair in self.logs:
            log_pair.render(surface)

        for star in self.stars:
            star.render(surface)

        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
