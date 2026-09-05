"""
ISPPV1-I2026
Study Case: Ultimate Fantasy (RPG)

This file contains the class PartyHealTargetState: pushed on top of
PartyActionState when a single-target heal action is selected. The player
picks a target party member using the cursor on the character names in
the bottom stats panel, then confirms with enter to apply the heal.
"""

from typing import Any, Dict

import pygame

from gale.state import BaseState

import settings


class PartyHealTargetState(BaseState):
    def enter(
        self,
        party_menu_state: Any,
        party_action_state: Any,
        caster: Any,
        action: Dict[str, Any],
    ) -> None:
        self.party_menu_state = party_menu_state
        self.party_action_state = party_action_state
        self.caster = caster
        self.action = action

        self.heal_target_index = party_menu_state.selected_char_index

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "party_menu":
            self.state_machine.pop()
            self.state_machine.pop()
            self.state_machine.pop()
            return

        if input_id == "move_left":
            self.heal_target_index = (self.heal_target_index - 1) % len(
                self.party_menu_state.characters
            )
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "move_right":
            self.heal_target_index = (self.heal_target_index + 1) % len(
                self.party_menu_state.characters
            )
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "enter":
            self._resolve_heal()
        elif input_id in ("move_up", "move_down"):
            self.state_machine.pop()

    def _resolve_heal(self) -> None:
        _, target = self.party_menu_state.characters[self.heal_target_index]
        action = self.action

        amount = action["func"](self.caster, target, action.get("strength"))
        settings.SOUNDS[action["sound_effect"]].play()

        from src.states.game.PartyMessageState import PartyMessageState

        self.state_machine.pop()
        self.state_machine.push(
            PartyMessageState(self.state_machine),
            party_menu_state=self.party_menu_state,
            party_action_state=self.party_action_state,
            message=f"{action['name']} for {amount} HP to {target.name}.",
        )

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.party_menu_state.render_stats_panel(
            surface, highlight_index=self.heal_target_index
        )
        self.party_action_state.render_actions_panel(surface)
