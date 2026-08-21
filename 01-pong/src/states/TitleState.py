import random
import pygame

import settings

from gale.state import BaseState
from gale.text import render_text
from gale.input_handler import InputData, KeyboardData

from src.rendering import render_table


class TitleState(BaseState):
    def enter(self, pong, *args, **kwargs) -> None:
        self.pong = pong

    def render(self, surface: pygame.Surface) -> None:
        render_table(surface, self.pong)
        render_text(
            surface,
            "Press Enter to start",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            pygame.Color(settings.COLOR_WHITE),
            center=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if isinstance(input_data, KeyboardData):
            if input_id == "confirm" and input_data.pressed:
                self.pong.serving_player = random.randint(1, 2)
                self.state_machine.change("serve", pong=self.pong)
