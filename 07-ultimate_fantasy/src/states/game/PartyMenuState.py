"""
ISPPV1 2023
Study Case: Ultimate Fantasy (RPG)

This file contains the class PartyMenuState: pushed on top of PlayState
when the player presses Tab during overworld exploration. It displays a
bottom-of-screen panel showing each party member's stats (sprite, name,
level, HP, ATK, DEF, MAG). The player selects a character with left/right
and presses enter to push PartyActionState for that character's actions.
"""

import math
from typing import Any, List

import pygame

from gale.state import BaseState

import settings
from src.definitions.entity import DEFAULT_CHARACTER_FRAME
from src.gui.Panel import Panel


class PartyMenuState(BaseState):
    def enter(self, play_state: Any) -> None:
        self.play_state = play_state
        self.party = play_state.world.party

        self.characters: List[tuple] = [
            (k, c) for k, c in sorted(self.party.characters.items()) if not c.dead
        ]

        if not self.characters:
            self.state_machine.pop()
            return

        self.selected_char_index = 0

        self.panel_height = 64
        self.panel_y = settings.VIRTUAL_HEIGHT - self.panel_height
        self.panel = Panel(0, self.panel_y, settings.VIRTUAL_WIDTH, self.panel_height)

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "party_menu":
            self.state_machine.pop()
            return

        if input_id == "move_left":
            self.selected_char_index = (self.selected_char_index - 1) % len(
                self.characters
            )
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "move_right":
            self.selected_char_index = (self.selected_char_index + 1) % len(
                self.characters
            )
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "enter":
            self._open_actions()

    def _open_actions(self) -> None:
        _, character = self.characters[self.selected_char_index]

        if not character.actions:
            return

        from src.states.game.PartyActionState import PartyActionState

        self.state_machine.push(
            PartyActionState(self.state_machine),
            party_menu_state=self,
            character=character,
        )

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.render_stats_panel(surface)

    def render_stats_panel(self, surface: pygame.Surface, highlight_index: int = None) -> None:
        """Render the bottom stats panel.

        Args:
            highlight_index: if provided, highlights this character index
                instead of self.selected_char_index (used by heal target
                selection).
        """
        self.panel.render(surface)

        if not self.characters:
            return

        if highlight_index is None:
            highlight_index = self.selected_char_index

        font = settings.FONTS["small"]
        num_chars = len(self.characters)
        col_width = settings.VIRTUAL_WIDTH // num_chars

        for i, (k, character) in enumerate(self.characters):
            col_x = i * col_width
            col_center_x = col_x + col_width // 2

            stats_offset_x  = -20
            sprite_offset_x = -10 + stats_offset_x

            sprite_frame = settings.frame(
                character.texture, DEFAULT_CHARACTER_FRAME
            )
            sprite_x = col_center_x - character.width // 2 + sprite_offset_x
            sprite_y = self.panel_y + 6
            surface.blit(
                settings.TEXTURES[character.texture],
                (sprite_x, sprite_y),
                sprite_frame,
            )

            name_surface = font.render(character.name, True, (255, 255, 255))
            name_rect = name_surface.get_rect(
                centerx=col_center_x + sprite_offset_x, top=sprite_y + character.height + 2
            )
            surface.blit(name_surface, name_rect)

            stats_x = col_center_x + character.width // 2 + 6 + stats_offset_x
            stats_y = self.panel_y + 8

            level_text = font.render(f"Lv.{character.level}", True, (255, 255, 100))
            surface.blit(level_text, (stats_x, stats_y))

            hp_color = (189, 32, 32) if character.current_hp < character.hp * 0.3 else (255, 255, 255)
            hp_text = font.render(
                f"HP:{math.floor(character.current_hp)}/{math.floor(character.hp)}",
                True,
                hp_color,
            )
            surface.blit(hp_text, (stats_x, stats_y + 10))

            atk_text = font.render(
                f"ATK:{math.floor(character.attack)}", True, (255, 200, 150)
            )
            surface.blit(atk_text, (stats_x, stats_y + 20))

            def_text = font.render(
                f"DEF:{math.floor(character.defense)}", True, (150, 200, 255)
            )
            surface.blit(def_text, (stats_x, stats_y + 30))

            mag_text = font.render(
                f"MAG:{math.floor(character.magic)}", True, (200, 150, 255)
            )
            surface.blit(mag_text, (stats_x, stats_y + 40))

            if i == highlight_index:
                cursor_x = sprite_x - 10
                cursor_y = sprite_y + character.height // 2 - 4
                surface.blit(
                    settings.TEXTURES["cursor-right"], (cursor_x, cursor_y)
                )
