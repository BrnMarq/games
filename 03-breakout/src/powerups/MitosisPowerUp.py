from typing import TypeVar

from src.powerups.PowerUp import PowerUp


class MitosisPowerUp(PowerUp):
    """
    Power-up that grants a mitosis charge. Press the action button to split
    all balls into three: one angled left, one angled right, and one opposite.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 1)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.mitosis_charges += 1

        for ball in play_state.balls:
            ball.start_blink()

        self.active = False
