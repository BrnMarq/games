"""
ISPPV1 2023
Study Case: Ultimate Fantasy (RPG)

This file contains the class PartyActionState: pushed on top of
PartyMenuState when the player selects a character. It shows the
character's actions list — heal-type actions (target_type == "character")
are selectable, while combat-only actions (target_type == "enemy") are
rendered semi-transparent and cannot be confirmed.
"""

from typing import Any, Dict, List

import pygame

from gale.state import BaseState

import settings
from src.gui.Panel import Panel


class PartyActionState(BaseState):
    def enter(self, party_menu_state: Any, character: Any) -> None:
        self.party_menu_state = party_menu_state
        self.character = character

        self.actions: List[Dict[str, Any]] = list(character.actions)
        self.usable_actions: List[bool] = [
            action["target_type"] == "character" for action in self.actions
        ]

        self.selected_action_index = 0
        self._snap_to_usable_action()

        action_panel_width = 120
        action_panel_height = len(self.actions) * 14 + 10
        self.actions_panel = Panel(
            settings.VIRTUAL_WIDTH - action_panel_width - 4,
            self.party_menu_state.panel_y - action_panel_height - 4,
            action_panel_width,
            action_panel_height,
        )

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "party_menu":
            self.state_machine.pop()
            self.state_machine.pop()
            return

        if input_id == "move_up":
            self._navigate(-1)
        elif input_id == "move_down":
            self._navigate(1)
        elif input_id == "enter":
            self._confirm()
        elif input_id in ("move_left", "move_right"):
            self.state_machine.pop()

    def _navigate(self, direction: int) -> None:
        if not self.actions:
            return

        self.selected_action_index = (
            self.selected_action_index + direction
        ) % len(self.actions)

        settings.SOUNDS["blip"].stop()
        settings.SOUNDS["blip"].play()

    def _snap_to_usable_action(self) -> None:
        if not self.actions:
            return

        if self.usable_actions[self.selected_action_index]:
            return

        for i in range(len(self.actions)):
            if self.usable_actions[i]:
                self.selected_action_index = i
                return

    def _confirm(self) -> None:
        if not self.actions:
            return

        if not self.usable_actions[self.selected_action_index]:
            return

        action = self.actions[self.selected_action_index]

        if action["require_target"]:
            from src.states.game.PartyHealTargetState import PartyHealTargetState

            self.state_machine.push(
                PartyHealTargetState(self.state_machine),
                party_menu_state=self.party_menu_state,
                party_action_state=self,
                caster=self.character,
                action=action,
            )
        else:
            alive_targets = [c for _, c in self.party_menu_state.characters]
            amount = action["func"](self.character, alive_targets, action.get("strength"))
            settings.SOUNDS[action["sound_effect"]].play()

            from src.states.game.PartyMessageState import PartyMessageState

            self.state_machine.push(
                PartyMessageState(self.state_machine),
                party_menu_state=self.party_menu_state,
                party_action_state=self,
                message=f"{action['name']} for {amount} HP to each ally.",
            )

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.party_menu_state.render_stats_panel(surface)
        self._render_actions_panel(surface)

    def _render_actions_panel(self, surface: pygame.Surface) -> None:
        self.actions_panel.render(surface)

        font = settings.FONTS["small"]
        panel_x = self.actions_panel.x + 8
        panel_y = self.actions_panel.y + 6

        for i, action in enumerate(self.actions):
            usable = self.usable_actions[i]
            is_selected = i == self.selected_action_index

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

    def render_actions_panel(self, surface: pygame.Surface) -> None:
        """Public accessor for child states that need to render this panel."""
        self._render_actions_panel(surface)
