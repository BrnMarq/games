"""
ISPPV1-I2026
Study Case: Super Martian (Platformer)

Author: Brian Marquez
brnmarq@gmail.com

This file contains the base class BaseEntityState.
"""

from typing import TypeVar

from gale.state import BaseState, StateMachine


class BaseEntityState(BaseState):
    def __init__(
        self, entity: TypeVar("GameEntity"), state_machine: StateMachine
    ) -> None:
        super().__init__(state_machine)
        self.entity = entity
