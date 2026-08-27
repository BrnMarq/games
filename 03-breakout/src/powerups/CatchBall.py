import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp


class CatchBall(PowerUp):
    """
    Power-up that lets the paddle catch and hold the ball.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 7)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle

        paddle.can_catch = True

        self.active = False
