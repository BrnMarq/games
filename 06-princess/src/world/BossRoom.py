"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class BossRoom — a special room containing a single
boss entity and no other objects. The entry door stays closed until the boss
is defeated.
"""

from typing import Callable, TypeVar

import settings
from src.definitions.entity import ENTITY_DEFS
from src.Entity import Entity
from src.states.entity.boss.BossIdleState import BossIdleState
from src.states.entity.boss.BossWalkState import BossWalkState
from src.states.entity.boss.BossAttackState import BossAttackState
from src.states.entity.boss.BossStunnedState import BossStunnedState
from src.world.Room import Room


class BossRoom(Room):
    def __init__(
        self,
        player: TypeVar("Player"),
        on_game_over: Callable[[], None],
        entry_direction: str,
    ) -> None:
        # Must be set before super().__init__ because it calls
        # _generate_entities / _generate_objects (overridden below).
        self.entry_direction = entry_direction
        self.boss_defeated = False

        super().__init__(player, on_game_over)

        # Keep only the entry doorway so the other three walls look like
        # plain walls with no door frames.
        self.doorways = [
            d for d in self.doorways if d.direction == self.entry_direction
        ]
        self._doorways_by_direction = {
            d.direction: d for d in self.doorways
        }

    # ------------------------------------------------------------------
    # Generation overrides
    # ------------------------------------------------------------------

    def _generate_entities(self) -> None:
        """Spawn a single boss entity in the centre of the room."""
        definition = ENTITY_DEFS["boss"]

        boss = Entity(
            x=settings.VIRTUAL_WIDTH / 2 - 8,
            y=settings.VIRTUAL_HEIGHT / 2 - 11,
            width=16,
            height=22,
            walk_speed=definition["walk_speed"],
            health=10,
            animation_defs=definition["animations"],
            states={},
        )
        boss.contact_damage = 2
        boss.offset_y = 5
        boss.is_boss = True
        boss.sword_invulnerable = True

        # Give the boss a back-reference to the room so its states can
        # access enemy_projectiles / player without passing room through
        # every enter() call.
        boss.room = self

        boss.state_machine.states = {
            "walk": lambda sm, e=boss: BossWalkState(e, sm),
            "idle": lambda sm, e=boss: BossIdleState(e, sm),
            "attack": lambda sm, e=boss: BossAttackState(e, sm),
            "stunned": lambda sm, e=boss: BossStunnedState(e, sm),
        }
        boss.change_state("idle")

        self.entities.append(boss)

    def _generate_objects(self) -> None:
        """No switches, pots, or chests in the boss room."""
        pass

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt: float) -> None:
        super().update(dt)

        # When the boss dies, open the entry door so the player can leave.
        if not self.boss_defeated and not self.entities:
            self.boss_defeated = True
            for doorway in self.doorways:
                if doorway.direction == self.entry_direction:
                    doorway.open = True
            settings.SOUNDS["door"].play()
    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def render(
        self,
        surface: pygame.Surface,
        camera_offset_x: float = 0,
        camera_offset_y: float = 0,
    ) -> None:
        super().render(surface, camera_offset_x, camera_offset_y)

        if not self.boss_defeated and self.entities:
            boss = self.entities[0]
            font = settings.FONTS["princess-small"]
            
            # Use red text if vulnerable, white if invulnerable
            color = settings.COLOR_TITLE if not boss.sword_invulnerable else settings.COLOR_WHITE
            
            text = font.render(f"Boss HP: {boss.health}/10", True, color)
            x = settings.VIRTUAL_WIDTH // 2 - text.get_width() // 2
            y = 10
            
            shadow = font.render(f"Boss HP: {boss.health}/10", True, settings.COLOR_TITLE_SHADOW)
            surface.blit(shadow, (x + 1, y + 1))
            surface.blit(text, (x, y))
