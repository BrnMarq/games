"""
ISPPV1-I2026
Study Case: Flappy Bird

Author: Brian Marquez
brnmarq@gmail.com

This file contains the definition of the class PlayingState.
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
from src.Bird import Bird
from src.World import World

from src.gamemodes import GameModeStrategy


class PauseState(BaseState):
    def enter(
        self,
        world: World,
        bird: Bird,
        score: int,
        gamemode: type[GameModeStrategy],
        *args,
        **kwargs,
    ) -> None:
        self.world = world
        self.bird = bird
        self.score = score
        self.gamemode = gamemode

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            pygame.Color(settings.COLOR_WHITE),
            shadowed=True,
        )
        render_text(
            surface,
            "Paused",
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            pygame.Color(settings.COLOR_WHITE),
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if isinstance(input_data, (KeyboardData, MouseClickData, GamepadButtonData)):
            if input_id == "pause" and input_data.pressed:
                self.state_machine.change(
                    "playing",
                    world=self.world,
                    bird=self.bird,
                    score=self.score,
                    gamemode=self.gamemode,
                )
