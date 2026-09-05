"""
ISPPV1-I2026
Study Case: The Legend of the Princess (ARPG)

This file contains the class BossIdleState.
"""

import random
from typing import TypeVar

import pygame

from src.states.entity.BaseEntityState import BaseEntityState


class BossIdleState(BaseEntityState):
    def enter(self) -> None:
        self.entity.offset_y = 5
        self.entity.offset_x = 0
        self.entity.change_animation(f"idle-{self.entity.direction}")

        # Short pause before resuming movement.
        self.wait_duration = random.uniform(0.5, 1.0)
        self.wait_timer = 0

    def process_ai(self, room: TypeVar("Room"), dt: float) -> None:
        self.wait_timer += dt

        if self.wait_timer > self.wait_duration:
            self.entity.change_state("walk")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
