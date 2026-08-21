import pygame

from gale.game import Game
from gale.input_handler import InputData, KeyboardData
from gale.state import BaseState, StateMachine

from src.Paddle import Paddle
from src.Ball import Ball
from src.rendering import render_table
from typing import Dict, Type

from src import states
import settings


class Pong(Game):
    def init(self) -> None:
        self.player1: Paddle = Paddle(
            settings.PADDLE_X_OFFSET,
            settings.PADDLE_Y_OFFSET,
            settings.PADDLE_WIDTH,
            settings.PADDLE_HEIGHT,
        )
        self.player2: Paddle = Paddle(
            settings.VIRTUAL_WIDTH - settings.PADDLE_WIDTH - settings.PADDLE_X_OFFSET,
            settings.VIRTUAL_HEIGHT - settings.PADDLE_HEIGHT - settings.PADDLE_Y_OFFSET,
            settings.PADDLE_WIDTH,
            settings.PADDLE_HEIGHT,
        )
        self.ball: Ball = Ball(
            settings.VIRTUAL_WIDTH / 2 - settings.BALL_SIZE / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BALL_SIZE / 2,
            settings.BALL_SIZE,
            settings.BALL_SIZE,
        )
        self.p1_score: int = 0
        self.p2_score: int = 0

        self.serving_player = 1
        self.winning_player = 0

        machine_states = {
            "title": states.TitleState,
            "serve": states.ServeState,
            "play": states.PlayState,
            "done": states.DoneState,
        }
        self.state_machine = StateMachine(machine_states)

        self.state_machine.change("title", pong=self)  # type: ignore

    def update(self, dt) -> None:
        self.state_machine.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)
        self.state_machine.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if isinstance(input_data, KeyboardData):
            if input_id == "quit" and input_data.pressed:
                quit()
            else:
                self.state_machine.on_input(input_id, input_data)
