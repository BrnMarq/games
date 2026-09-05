"""
ISPPV1-I2026
Study Case: Flappy Bird

Author: Brian Marquez
brnmarq@gmail.com

This file contains the definition of the class CountDownState.
"""

import pygame

from typing import Optional
from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World

from src.gamemodes import GameModeStrategy, NormalMode


class CountDownState(BaseState):
    def enter(
        self, gamemode: Optional[type[GameModeStrategy]] = None, *args, **kwargs
    ) -> None:
        self.world = World()
        self.gamemode = gamemode
        self.counter = 3
        self.timer = 0.0

    def update(self, dt: float) -> None:
        self.timer += dt

        if self.timer >= 1.0:
            self.timer = 0.0
            self.counter -= 1

            if self.counter == 0:
                self.state_machine.change(
                    "playing", world=self.world, gamemode=self.gamemode
                )
                return

        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            str(self.counter),
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            pygame.Color(settings.COLOR_WHITE),
            center=True,
            shadowed=True,
        )
