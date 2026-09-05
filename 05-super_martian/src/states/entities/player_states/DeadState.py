"""
ISPPV1-I2026
Study Case: Super Martian (Platformer)

Author: Brian Marquez
brnmarq@gmail.com

This file contains the class DeadState for player.
"""

from src.states.entities.BaseEntityState import BaseEntityState


class DeadState(BaseEntityState):
    def enter(self) -> None:
        self.entity.is_dead = True
