"""
ISPPV1 2023
Study Case: Ultimate Fantasy (RPG)

This file contains the class PartyMenuState: pushed on top of PlayState
when the player presses Tab during overworld exploration. It displays a
bottom-of-screen panel showing each party member's stats (sprite, name,
level, HP, ATK, DEF, MAG). The player can select a character to view
their actions — heal-type actions (target_type == "character") are
usable, while combat-only actions (target_type == "enemy") are rendered
semi-transparent and cannot be selected.
"""

import math
from typing import Any, Dict, List, Optional

import pygame

from gale.state import BaseState
from gale.timer import Timer

import settings
from src.definitions.entity import DEFAULT_CHARACTER_FRAME
from src.gui.Panel import Panel


# Sub-states within the PartyMenuState
_MODE_CHARACTER_SELECT = 0
_MODE_ACTION_SELECT = 1
_MODE_HEAL_TARGET_SELECT = 2


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

        self.mode = _MODE_CHARACTER_SELECT
        self.selected_char_index = 0

        self.selected_action_index = 0
        self.actions: List[Dict[str, Any]] = []
        self.usable_actions: List[bool] = []

        self.heal_target_index = 0
        self.pending_action: Optional[Dict[str, Any]] = None

        self.message: Optional[str] = None
        self.message_timer = 0.0

        self.panel_height = 64
        self.panel_y = settings.VIRTUAL_HEIGHT - self.panel_height
        self.panel = Panel(0, self.panel_y, settings.VIRTUAL_WIDTH, self.panel_height)

        self.actions_panel: Optional[Panel] = None

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "party_menu":
            self.state_machine.pop()
            return

        if self.message:
            if input_id == "enter":
                self.message = None
            return

        if self.mode == _MODE_CHARACTER_SELECT:
            self._input_character_select(input_id)
        elif self.mode == _MODE_ACTION_SELECT:
            self._input_action_select(input_id)
        elif self.mode == _MODE_HEAL_TARGET_SELECT:
            self._input_heal_target_select(input_id)

    def _input_character_select(self, input_id: str) -> None:
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

    def _input_action_select(self, input_id: str) -> None:
        if input_id == "move_up":
            self._navigate_action(-1)
        elif input_id == "move_down":
            self._navigate_action(1)
        elif input_id == "enter":
            self._confirm_action()
        elif input_id == "move_left" or input_id == "move_right":
            self._close_actions()

    def _input_heal_target_select(self, input_id: str) -> None:
        if input_id == "move_left":
            self.heal_target_index = (self.heal_target_index - 1) % len(
                self.characters
            )
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "move_right":
            self.heal_target_index = (self.heal_target_index + 1) % len(
                self.characters
            )
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "enter":
            self._resolve_heal()
        elif input_id == "move_up" or input_id == "move_down":
            self.mode = _MODE_ACTION_SELECT
            self.pending_action = None

    def _open_actions(self) -> None:
        _, character = self.characters[self.selected_char_index]
        self.actions = list(character.actions)

        if not self.actions:
            return

        self.usable_actions = [
            action["target_type"] == "character" for action in self.actions
        ]

        self.selected_action_index = 0
        self._snap_to_usable_action()

        self.mode = _MODE_ACTION_SELECT

        action_panel_width = 120
        action_panel_height = len(self.actions) * 14 + 10
        self.actions_panel = Panel(
            settings.VIRTUAL_WIDTH - action_panel_width - 4,
            self.panel_y - action_panel_height - 4,
            action_panel_width,
            action_panel_height,
        )

    def _close_actions(self) -> None:
        self.mode = _MODE_CHARACTER_SELECT
        self.actions = []
        self.usable_actions = []
        self.actions_panel = None

    def _navigate_action(self, direction: int) -> None:
        if not self.actions:
            return

        self.selected_action_index = (
            self.selected_action_index + direction
        ) % len(self.actions)

        settings.SOUNDS["blip"].stop()
        settings.SOUNDS["blip"].play()

    def _snap_to_usable_action(self) -> None:
        """Move selection to the nearest usable action if current is not usable."""
        if not self.actions:
            return

        if self.usable_actions[self.selected_action_index]:
            return

        for i in range(len(self.actions)):
            if self.usable_actions[i]:
                self.selected_action_index = i
                return

    def _confirm_action(self) -> None:
        if not self.actions:
            return

        if not self.usable_actions[self.selected_action_index]:
            return

        action = self.actions[self.selected_action_index]

        if action["require_target"]:
            self.pending_action = action
            self.heal_target_index = self.selected_char_index
            self.mode = _MODE_HEAL_TARGET_SELECT
        else:
            _, caster = self.characters[self.selected_char_index]
            alive_targets = [c for _, c in self.characters]
            amount = action["func"](caster, alive_targets, action.get("strength"))
            settings.SOUNDS[action["sound_effect"]].play()
            self.message = f"{action['name']} for {amount} HP to each ally."

    def _resolve_heal(self) -> None:
        if self.pending_action is None:
            return

        action = self.pending_action
        _, caster = self.characters[self.selected_char_index]
        _, target = self.characters[self.heal_target_index]

        amount = action["func"](caster, target, action.get("strength"))
        settings.SOUNDS[action["sound_effect"]].play()
        self.message = f"{action['name']} for {amount} HP to {target.name}."

        self.pending_action = None
        self.mode = _MODE_ACTION_SELECT

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self._render_stats_panel(surface)

        if self.mode == _MODE_ACTION_SELECT or self.mode == _MODE_HEAL_TARGET_SELECT:
            self._render_actions_panel(surface)

        if self.message:
            self._render_message(surface)

    def _render_stats_panel(self, surface: pygame.Surface) -> None:
        self.panel.render(surface)

        if not self.characters:
            return

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

            is_selected = (
                (self.mode == _MODE_CHARACTER_SELECT and i == self.selected_char_index)
                or (self.mode == _MODE_HEAL_TARGET_SELECT and i == self.heal_target_index)
            )
            if is_selected:
                cursor_x = sprite_x - 10
                cursor_y = sprite_y + character.height // 2 - 4
                surface.blit(
                    settings.TEXTURES["cursor-right"], (cursor_x, cursor_y)
                )

    def _render_actions_panel(self, surface: pygame.Surface) -> None:
        if self.actions_panel is None:
            return

        self.actions_panel.render(surface)

        font = settings.FONTS["small"]
        panel_x = self.actions_panel.x + 8
        panel_y = self.actions_panel.y + 6

        for i, action in enumerate(self.actions):
            usable = self.usable_actions[i]
            is_selected = (
                self.mode == _MODE_ACTION_SELECT
                and i == self.selected_action_index
            )

            if usable:
                color = (255, 255, 255)
            else:
                color = (120, 120, 120)

            text = action["name"]
            if not usable:
                text += " (Combat)"

            text_surface = font.render(text, True, color)

            if not usable:
                text_surface.set_alpha(100)

            y = panel_y + i * 14
            surface.blit(text_surface, (panel_x + 10, y))

            if is_selected and usable:
                surface.blit(
                    settings.TEXTURES["cursor-right"], (panel_x, y)
                )

    def _render_message(self, surface: pygame.Surface) -> None:
        font = settings.FONTS["small"]

        msg_panel = Panel(
            settings.VIRTUAL_WIDTH // 4,
            self.panel_y - 30,
            settings.VIRTUAL_WIDTH // 2,
            24,
        )
        msg_panel.render(surface)

        text_surface = font.render(self.message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            centerx=settings.VIRTUAL_WIDTH // 2,
            centery=self.panel_y - 30 + 12,
        )
        surface.blit(text_surface, text_rect)
