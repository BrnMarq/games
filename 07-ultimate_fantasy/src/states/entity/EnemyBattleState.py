"""
ISPPV1-I2026
Study Case: Ultimate Fantasy (RPG)

Author: Brian Marquez
brnmarq@gmail.com

This file contains the class EnemyBattleState. Actual action-selection AI
lives in TakeTurnState (a uniformly random choice among entity.actions,
guaranteed to hit a living target); this state just keeps the enemy's
idle/attack animation running.
"""

from src.states.entity.EntityBaseState import EntityBaseState


class EnemyBattleState(EntityBaseState):
    def enter(self) -> None:
        self.entity.change_animation("default")
