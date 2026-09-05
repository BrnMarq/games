"""
ISPPV1-I2026
Study Case: Super Martian (Platformer)

Author: Brian Marquez
brnmarq@gmail.com

This module contains all of the player states.
"""

from src.states.entities.player_states.DeadState import DeadState
from src.states.entities.player_states.FallState import FallState
from src.states.entities.player_states.IdleState import IdleState
from src.states.entities.player_states.JumpState import JumpState
from src.states.entities.player_states.WalkState import WalkState

(DeadState, FallState, IdleState, JumpState, WalkState)
