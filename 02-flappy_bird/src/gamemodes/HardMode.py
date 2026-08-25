import random

from .Strategy import GameModeStrategy

from gale.factory import Factory
from gale.input_handler import (
    InputData,
    KeyboardData,
    MouseClickData,
    GamepadButtonData,
)

from src.LogPair import LogPair
import settings


class HardMode(GameModeStrategy):
    def __init__(self, world, bird, score, state_machine):
        self.world = world
        self.bird = bird
        self.state_machine = state_machine
        self.score = score
        self.logs_spawn_timer: float = 0.0
        self.last_log_y: float = -settings.LOG_HEIGHT + random.randint(0, 80) + 20
        self.log_pair_factory: Factory = Factory(LogPair)

        self.time_to_next_log = settings.TIME_TO_SPAWN_LOGS

    def update(self, dt):
        self.bird.update(dt)
        self.world.update(dt)

        self.logs_spawn_timer += dt

        if self.logs_spawn_timer >= self.time_to_next_log:
            self.logs_spawn_timer = 0.0
            y = max(
                -settings.LOG_HEIGHT + 10,
                min(
                    self.last_log_y + random.randint(-20, 20),
                    settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT,
                ),
            )
            self.last_log_y = y

            gap = random.randint(settings.LOGS_GAP - 30, settings.LOGS_GAP)
            props = (
                {
                    "gap": gap,
                    "closing": True,
                }
                if random.random() < settings.CLOSING_LOGS_CHANCE / 100
                else {"gap": gap}
            )
            self.world.logs.append(
                self.log_pair_factory.create(settings.VIRTUAL_WIDTH, y, props)
            )
            self.time_to_next_log = random.uniform(1, 2)

        if self.world.collides(self.bird.get_rect()):
            settings.SOUNDS["explosion"].play()
            settings.SOUNDS["hurt"].play()
            self.state_machine.change("count_down", gamemode=type(self))
            return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if isinstance(input_data, (KeyboardData, MouseClickData, GamepadButtonData)):
            if input_data.pressed:
                match input_id:
                    case "jump":
                        self.bird.jump()
                    case "pause":
                        self.state_machine.change(
                            "pause",
                            world=self.world,
                            bird=self.bird,
                            score=self.score,
                            gamemode=type(self),
                        )
                    case "move_left":
                        self.bird.vx = -settings.BIRD_X_SPEED
                    case "move_right":
                        self.bird.vx = settings.BIRD_X_SPEED
            elif input_data.released:
                match input_id:
                    case "move_left":
                        if self.bird.vx == -settings.BIRD_X_SPEED:
                            self.bird.vx = 0
                    case "move_right":
                        if self.bird.vx == settings.BIRD_X_SPEED:
                            self.bird.vx = 0
