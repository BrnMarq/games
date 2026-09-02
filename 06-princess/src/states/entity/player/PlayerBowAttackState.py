"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayerBowAttackState.
"""

from typing import TypeVar

import pygame

from gale.state import StateMachine

import settings
from src.GameObject import GameObject
from src.Projectile import Projectile
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.states.entity.BaseEntityState import BaseEntityState


class PlayerBowAttackState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon

        # Render offset for spaced character sprite.
        self.entity.offset_y = 5
        self.entity.offset_x = 8

        self.entity.change_animation(f"bow-{self.entity.direction}")

    def enter(self) -> None:
        settings.SOUNDS["sword"].stop()
        settings.SOUNDS["sword"].play()

        # Restart bow animation.
        self.entity.current_animation.reset()

        # Spawn arrow projectile in front of the player.
        direction = self.entity.direction
        arrow = GameObject(
            GAME_OBJECT_DEFS["arrow"],
            self.entity.x + self.entity.width / 2 - 4,
            self.entity.y + self.entity.height / 2 - 4,
        )
        self.dungeon.current_room.projectiles.append(Projectile(arrow, direction))

    def update(self, dt: float) -> None:
        self.entity.interact_requested = False
        self.entity.sword_requested = False
        self.entity.bow_requested = False

        if self.entity.current_animation.times_played > 0:
            self.entity.current_animation.times_played = 0
            self.entity.change_state("idle")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
