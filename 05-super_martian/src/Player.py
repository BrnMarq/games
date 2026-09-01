"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Player.
"""

from typing import TypeVar

from gale.command import CommandBindings
from gale.input_handler import InputData

from src.GameEntity import GameEntity
from src.commands import (
    JUMP,
    MOVE_LEFT,
    MOVE_RIGHT,
    STOP_JUMP,
    STOP_MOVE_LEFT,
    STOP_MOVE_RIGHT,
)
from src.states.entities import player_states


class Player(GameEntity):
    def __init__(self, x: int, y: int, game_level: TypeVar("GameLevel")) -> None:
        super().__init__(
            x,
            y,
            16,
            20,
            "martian",
            game_level,
            states={
                "idle": lambda sm: player_states.IdleState(self, sm),
                "walk": lambda sm: player_states.WalkState(self, sm),
                "jump": lambda sm: player_states.JumpState(self, sm),
                "fall": lambda sm: player_states.FallState(self, sm),
                "dead": lambda sm: player_states.DeadState(self, sm),
            },
            animation_defs={
                "idle": {"frames": [0]},
                "walk": {"frames": [9, 10], "interval": 0.15},
                "jump": {"frames": [2]},
            },
        )
        self.score = 0
        self.coins_counter = {54: 0, 55: 0, 61: 0, 62: 0}
        self.key_picked = False

        self.command_bindings = CommandBindings()
        self.command_bindings.bind("move_left", press=MOVE_LEFT, release=STOP_MOVE_LEFT)
        self.command_bindings.bind(
            "move_right", press=MOVE_RIGHT, release=STOP_MOVE_RIGHT
        )
        self.command_bindings.bind("jump", press=JUMP, release=STOP_JUMP)

    def _check_key_block(self) -> None:
        row = int(self.y // self.tilemap.tile_height) - 1
        if row < 0:
            return

        min_col = int(self.x // self.tilemap.tile_width)
        max_col = int((self.x + self.width - 1e-6) // self.tilemap.tile_width)

        for col in range(min_col, max_col + 1):
            if not self.tilemap.in_bounds(row, col):
                continue
            gid = self.tilemap.get_gid(self.COLLISION_LAYER, row, col)
            if gid == 0:
                continue
            props = self.tilemap.properties_of_gid(gid)
            if props.get("key_block", False):
                block_x = col * self.tilemap.tile_width
                block_y = row * self.tilemap.tile_height
                self.game_level.spawn_key(block_x, block_y)
                return

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.block_hit_from_below:
            self._check_key_block()

    def on_input(self, input_id: str, input_data: InputData) -> None:
        self.command_bindings.dispatch(self, input_id, input_data)
