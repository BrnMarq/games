"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame

from gale.input_handler import (
    InputData,
    KeyboardData,
    MouseClickData,
    GamepadButtonData,
)
from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World


class TitleScreenState(BaseState):
    def enter(self, *args, **kwargs) -> None:
        self.world = World()

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            pygame.Color(settings.COLOR_WHITE),
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Press Enter to start",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2 * settings.VIRTUAL_HEIGHT / 3,
            pygame.Color(settings.COLOR_WHITE),
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if isinstance(input_data, (KeyboardData, MouseClickData, GamepadButtonData)):
            if input_id == "confirm" and input_data.pressed:
                self.state_machine.change("count_down")
