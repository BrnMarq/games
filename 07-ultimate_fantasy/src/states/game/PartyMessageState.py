"""
ISPPV1-I2026
Study Case: Ultimate Fantasy (RPG)

This file contains the class PartyMessageState: a simple message overlay
shown after a heal action resolves. Dismisses on enter, returning to the
action list.
"""

from typing import Any

import pygame

from gale.state import BaseState

import settings
from src.gui.Panel import Panel


class PartyMessageState(BaseState):
    def enter(
        self,
        party_menu_state: Any,
        party_action_state: Any,
        message: str,
    ) -> None:
        self.party_menu_state = party_menu_state
        self.party_action_state = party_action_state
        self.message = message

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "party_menu":
            self.state_machine.pop()
            self.state_machine.pop()
            self.state_machine.pop()
            return

        if input_id == "enter":
            self.state_machine.pop()

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.party_menu_state.render_stats_panel(surface)
        self.party_action_state.render_actions_panel(surface)

        font = settings.FONTS["small"]
        panel_y = self.party_menu_state.panel_y

        msg_panel = Panel(
            settings.VIRTUAL_WIDTH // 4,
            panel_y - 30,
            settings.VIRTUAL_WIDTH // 2,
            24,
        )
        msg_panel.render(surface)

        text_surface = font.render(self.message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            centerx=settings.VIRTUAL_WIDTH // 2,
            centery=panel_y - 30 + 12,
        )
        surface.blit(text_surface, text_rect)
