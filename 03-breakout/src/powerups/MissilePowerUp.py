from typing import TypeVar

from src.powerups.PowerUp import PowerUp


class MissilePowerUp(PowerUp):
    """
    Power-up that gives the paddle two missiles to fire.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 0)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.missiles = 2
        self.active = False
