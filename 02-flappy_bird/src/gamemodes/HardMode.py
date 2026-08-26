import random

import pygame

from .Strategy import GameModeStrategy

from gale.factory import Factory
from gale.input_handler import (
    InputData,
    KeyboardData,
    MouseClickData,
    GamepadButtonData,
)

from src.LogPair import LogPair
from src.powerups import Star
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
        self.star_factory: Factory = Factory(Star)

        self.time_to_next_log = settings.TIME_TO_SPAWN_LOGS
        self.star_spawn_timer: float = 0.0
        self.star_cooldown: float = 0.0
        self._prev_ghost_time: float = 0.0

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
                if random.random() * 100 < settings.CLOSING_LOGS_CHANCE
                else {"gap": gap}
            )
            self.world.logs.append(
                self.log_pair_factory.create(settings.VIRTUAL_WIDTH, y, props)
            )
            self.time_to_next_log = random.uniform(1, 2)

        self.star_cooldown -= dt

        if self.world.logs:
            last_log_x = self.world.logs[-1].x
            if (
                settings.VIRTUAL_WIDTH - (last_log_x + settings.LOG_WIDTH)
                > settings.STAR_SIZE * 2
            ):
                self.star_spawn_timer += dt
                if (
                    self.star_spawn_timer >= 1.0
                    and self.star_cooldown <= 0
                    and random.random() * 100 < settings.STAR_SPAWN_CHANCE
                ):
                    self.star_spawn_timer = 0.0
                    self.star_cooldown = 5.0
                    self.world.stars.append(
                        self.star_factory.create(
                            settings.VIRTUAL_WIDTH - settings.STAR_SIZE,
                            random.uniform(
                                0, settings.VIRTUAL_HEIGHT - settings.STAR_SIZE
                            ),
                        )
                    )

        if self._prev_ghost_time > 0 and self.bird.ghost_time_left <= 0:
            pygame.mixer.music.load(settings.NORMAL_MUSIC_PATH)
            pygame.mixer.music.play(loops=-1)

        self._prev_ghost_time = self.bird.ghost_time_left

        if self.world.collides_with_ground(self.bird.get_rect()) or (
            not (self.bird.ghost_time_left > 0)
            and self.world.collides_with_logs(self.bird.get_rect())
        ):
            settings.SOUNDS["explosion"].play()
            settings.SOUNDS["hurt"].play()
            self.state_machine.change("count_down", gamemode=type(self))
            return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

        if self.bird.ghost_time_left <= 0:
            star = self.world.collect_star(self.bird.get_rect())
            if star:
                self.bird.ghost_time_left = settings.GHOST_DURATION
                self.bird.start_ghost_pulse()
                pygame.mixer.music.load(settings.GHOST_MUSIC_PATH)
                pygame.mixer.music.play(loops=-1)

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
