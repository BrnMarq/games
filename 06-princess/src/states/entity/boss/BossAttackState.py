"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class BossAttackState.
"""

from typing import TypeVar

import pygame

from src.Fireball import Fireball
from src.states.entity.BaseEntityState import BaseEntityState


class BossAttackState(BaseEntityState):
    def enter(self) -> None:
        # Wider sprite offset for the 32×32 swing sheet.
        self.entity.offset_y = 5
        self.entity.offset_x = 8

        self.entity.change_animation(f"attack-{self.entity.direction}")
        self.entity.current_animation.reset()

        self.fireball_spawned = False

    def update(self, dt: float) -> None:
        # Spawn fireball on the first frame of the attack.
        if not self.fireball_spawned:
            self.fireball_spawned = True
            room = self.entity.room
            player = room.player

            fireball = Fireball(
                self.entity.x + self.entity.width / 2,
                self.entity.y + self.entity.height / 2,
                player.x + player.width / 2,
                player.y + player.height / 2,
            )
            room.enemy_projectiles.append(fireball)

        # Wait for the swing animation to finish.
        if self.entity.current_animation.times_played > 0:
            self.entity.current_animation.times_played = 0
            self.entity.change_state("idle")

    def process_ai(self, room: TypeVar("Room"), dt: float) -> None:
        # No AI decisions while the attack animation plays.
        pass

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
