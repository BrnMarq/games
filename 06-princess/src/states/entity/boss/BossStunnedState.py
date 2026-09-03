"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class BossStunnedState.
"""

from typing import TypeVar

import pygame

from src.states.entity.BaseEntityState import BaseEntityState


class BossStunnedState(BaseEntityState):
    def enter(self) -> None:
        self.entity.offset_y = 5
        self.entity.offset_x = 0
        self.entity.change_animation(f"idle-{self.entity.direction}")

    def process_ai(self, room: TypeVar("Room"), dt: float) -> None:
        # The Entity update method manages the sword_invulnerability_timer.
        # Once the vulnerability expires, the boss recovers from the stun.
        if self.entity.sword_invulnerable:
            self.entity.change_state("idle")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
