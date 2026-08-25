"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World

from src.gamemodes import GameModeStrategy, NormalMode, HardMode


class PlayingState(BaseState):
    def enter(
        self,
        world: Optional[World] = None,
        bird: Optional[Bird] = None,
        score: int = 0,
        gamemode: Optional[type[GameModeStrategy]] = None,
        *args,
        **kwargs,
    ) -> None:
        self.world = world if world is not None else World()
        self.world.reset(True)
        self.bird = (
            bird
            if bird is not None
            else Bird(
                settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
                settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
                settings.BIRD_WIDTH,
                settings.BIRD_HEIGHT,
            )
        )
        self.strategy = (
            gamemode
            if gamemode is not None
            else NormalMode(self.world, self.bird, score, self.state_machine)
        )

    def update(self, dt: float) -> None:
        self.strategy.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.strategy.score}",
            settings.FONTS["flappy"],
            20,
            10,
            pygame.Color(settings.COLOR_WHITE),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        self.strategy.on_input(input_id, input_data)
