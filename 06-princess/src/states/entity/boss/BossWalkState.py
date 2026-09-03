"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class BossWalkState.
"""

import random
from typing import TypeVar

import pygame

from src import commands
from src.states.entity.BaseEntityState import BaseEntityState
from src.states.entity.movement import move_and_bump

_MOVE_COMMANDS = {
    "left": commands.MOVE_LEFT,
    "right": commands.MOVE_RIGHT,
    "up": commands.MOVE_UP,
    "down": commands.MOVE_DOWN,
}
_STOP_COMMANDS = (
    commands.STOP_MOVE_LEFT,
    commands.STOP_MOVE_RIGHT,
    commands.STOP_MOVE_UP,
    commands.STOP_MOVE_DOWN,
)


class BossWalkState(BaseEntityState):
    def enter(self) -> None:
        self.entity.offset_y = 5
        self.entity.offset_x = 0
        self.entity.change_animation(f"walk-{self.entity.direction}")

        # How long before re-aiming at the player.
        self.move_duration = random.uniform(0.5, 1.5)
        self.movement_timer = 0

        # Fireball cooldown: 2–3 seconds.
        self.fireball_cooldown = random.uniform(2, 3)
        self.fireball_timer = 0

        self.bumped = False

    def update(self, dt: float) -> None:
        entity = self.entity
        held = entity.held

        if held["move_left"]:
            entity.direction = "left"
        elif held["move_right"]:
            entity.direction = "right"
        elif held["move_up"]:
            entity.direction = "up"
        elif held["move_down"]:
            entity.direction = "down"

        entity.change_animation(f"walk-{entity.direction}")
        self.bumped = move_and_bump(entity, dt)

    def process_ai(self, room: TypeVar("Room"), dt: float) -> None:
        self.fireball_timer += dt
        self.movement_timer += dt

        # Time to attack?
        if self.fireball_timer >= self.fireball_cooldown:
            self.entity.change_state("attack")
            return

        # Re-aim toward the player periodically or when bumping a wall.
        if self.movement_timer > self.move_duration or self.bumped:
            self.movement_timer = 0
            self.move_duration = random.uniform(0.5, 1.5)
            self._aim_at_player(room.player)

    def _aim_at_player(self, player) -> None:
        # Release all held directions.
        for stop in _STOP_COMMANDS:
            stop.execute(self.entity)

        dx = player.x - self.entity.x
        dy = player.y - self.entity.y

        if abs(dx) > abs(dy):
            direction = "right" if dx > 0 else "left"
        else:
            direction = "down" if dy > 0 else "up"

        _MOVE_COMMANDS[direction].execute(self.entity)
        self.entity.change_animation(f"walk-{direction}")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
