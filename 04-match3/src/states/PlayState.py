"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List, Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Drag state
        self.dragging = False
        self.drag_start_i = -1
        self.drag_start_j = -1
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_tile = None

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

    def render(self, surface: pygame.Surface) -> None:
        # Render all tiles except the dragged one
        for row in self.board.tiles:
            for tile in row:
                if tile is not self.drag_tile:
                    tile.render(surface, self.board.x, self.board.y)

        # Render dragged tile last (on top of everything)
        if self.dragging and self.drag_tile:
            self.drag_tile.render(surface, self.board.x, self.board.y)

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        # Debug: spawn powerup on random tile
        if input_id == "enter" and input_data.pressed:
            import random

            i = random.randint(0, settings.BOARD_HEIGHT - 1)
            j = random.randint(0, settings.BOARD_WIDTH - 1)
            self.board.tiles[i][j].powerup = "line_clear"
            print(f"Debug: Powerup spawned at ({i}, {j})")
            return

        # Debug: force a 4-tile match at row 3
        if input_id == "up" and input_data.pressed:
            row = 3
            color = self.board.tiles[row][0].color
            for j in range(4):
                if j == 2:
                    self.board.tiles[row + 1][j].color = color
                else:
                    self.board.tiles[row][j].color = color
            print(f"Debug: Forced 4-tile match at row {row}")
            return

        # Debug: spawn bomb powerup on random tile
        if input_id == "down" and input_data.pressed:
            row = 3
            color = self.board.tiles[row][0].color
            for j in range(5):
                if j == 2:
                    self.board.tiles[row + 1][j].color = color
                else:
                    self.board.tiles[row][j].color = color
            print(f"Debug: Forced 4-tile match at row {row}")
            return

        if input_id == "click" and input_data.pressed:
            if not self.active:
                return

            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            i = (pos_y - self.board.y) // settings.TILE_SIZE
            j = (pos_x - self.board.x) // settings.TILE_SIZE

            if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                self.dragging = True
                self.drag_start_i = i
                self.drag_start_j = j
                self.drag_tile = self.board.tiles[i][j]
                self.drag_start_x = self.drag_tile.x
                self.drag_start_y = self.drag_tile.y
                self.active = False

        elif input_id == "mouse_motion" and self.dragging:
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            self.drag_tile.x = pos_x - self.board.x - settings.TILE_SIZE // 2
            self.drag_tile.y = pos_y - self.board.y - settings.TILE_SIZE // 2

        elif input_id == "click" and input_data.released and self.dragging:
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            # Check if this was a tap (minimal movement) on a powerup tile
            dx = pos_x - (self.drag_start_x + self.board.x + settings.TILE_SIZE // 2)
            dy = pos_y - (self.drag_start_y + self.board.y + settings.TILE_SIZE // 2)
            dist = (dx**2 + dy**2) ** 0.5

            if (
                dist < 5
                and self.drag_tile
                and self.drag_tile.powerup in ("line_clear", "bomb")
            ):
                tile = self.drag_tile
                self.dragging = False
                self.drag_tile = None
                if tile.powerup == "line_clear":
                    self._activate_line_clear(tile)
                else:
                    self._activate_bomb(tile)
                return

            end_i = (pos_y - self.board.y) // settings.TILE_SIZE
            end_j = (pos_x - self.board.x) // settings.TILE_SIZE

            di = abs(end_i - self.drag_start_i)
            dj = abs(end_j - self.drag_start_j)

            if (
                di <= 1
                and dj <= 1
                and di != dj
                and 0 <= end_i < settings.BOARD_HEIGHT
                and 0 <= end_j < settings.BOARD_WIDTH
            ):
                tile1 = self.drag_tile
                tile2 = self.board.tiles[end_i][end_j]

                orig_x1, orig_y1 = self.drag_start_x, self.drag_start_y
                orig_x2, orig_y2 = tile2.x, tile2.y

                # Temporarily swap in grid + indices to check for matches
                (
                    self.board.tiles[self.drag_start_i][self.drag_start_j],
                    self.board.tiles[end_i][end_j],
                ) = (tile2, tile1)
                tile1.i, tile1.j, tile2.i, tile2.j = (
                    end_i,
                    end_j,
                    self.drag_start_i,
                    self.drag_start_j,
                )

                self.board.matches = []
                has_match = self.board.calculate_matches_for([tile1, tile2]) is not None

                # Swap back in grid + indices (restore state)
                (
                    self.board.tiles[self.drag_start_i][self.drag_start_j],
                    self.board.tiles[end_i][end_j],
                ) = (tile1, tile2)
                tile1.i, tile1.j, tile2.i, tile2.j = (
                    self.drag_start_i,
                    self.drag_start_j,
                    end_i,
                    end_j,
                )
                self.board.matches = []

                if has_match:
                    # Valid move — animate the swap
                    moved_tile = self.drag_tile

                    def arrive():
                        tile1 = self.board.tiles[self.drag_start_i][self.drag_start_j]
                        tile2 = self.board.tiles[end_i][end_j]
                        (
                            self.board.tiles[tile1.i][tile1.j],
                            self.board.tiles[tile2.i][tile2.j],
                        ) = (
                            self.board.tiles[tile2.i][tile2.j],
                            self.board.tiles[tile1.i][tile1.j],
                        )
                        tile1.i, tile1.j, tile2.i, tile2.j = (
                            tile2.i,
                            tile2.j,
                            tile1.i,
                            tile1.j,
                        )
                        self._calculate_matches([tile1, tile2], moved_tile)

                    Timer.tween(
                        0.25,
                        [
                            (tile1, {"x": orig_x2, "y": orig_y2}),
                            (tile2, {"x": orig_x1, "y": orig_y1}),
                        ],
                        on_finish=arrive,
                    )
                else:
                    # No match — snap back
                    settings.SOUNDS["error"].play()

                    def on_snap_back():
                        self.dragging = False
                        self.drag_tile = None
                        self.active = True

                    Timer.tween(
                        0.15,
                        [
                            (
                                self.drag_tile,
                                {"x": self.drag_start_x, "y": self.drag_start_y},
                            )
                        ],
                        on_finish=on_snap_back,
                    )
            else:
                # Not adjacent — snap back
                settings.SOUNDS["error"].play()

                def on_snap_back():
                    self.dragging = False
                    self.drag_tile = None
                    self.active = True

                Timer.tween(
                    0.15,
                    [
                        (
                            self.drag_tile,
                            {"x": self.drag_start_x, "y": self.drag_start_y},
                        )
                    ],
                    on_finish=on_snap_back,
                )

            self.dragging = False
            self.drag_tile = None

    def _calculate_matches(self, tiles: List, moved_tile: Optional[any] = None) -> bool:
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            while not self.board.has_valid_move():
                self.board._initialize_tiles()

            self.active = True
            return False

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        extra_destroyed = []
        activated_powerups = []

        for match in matches:
            self.score += len(match) * 50

            # Check for powerup tiles in this match and activate them
            for tile in match:
                if tile.powerup == "line_clear":
                    targets = self.board.get_line_clear_targets(tile)
                    extra_destroyed.extend(targets)
                    activated_powerups.append(tile)
                elif tile.powerup == "bomb":
                    targets = self.board.get_bomb_targets(tile)
                    extra_destroyed.extend(targets)
                    activated_powerups.append(tile)

            # Check if this is a 4-tile match and create powerup on moved tile
            if len(match) == 4 and moved_tile is not None and moved_tile in match:
                moved_tile.powerup = "line_clear"
            # Check if this is a 5-tile match and create bomb on moved tile
            elif len(match) >= 5 and moved_tile is not None and moved_tile in match:
                moved_tile.powerup = "bomb"

        # Clear powerup attribute so remove_matches() will remove them
        for tile in activated_powerups:
            tile.powerup = None

        self.board.remove_matches()

        # Remove extra tiles from powerup activations
        for tile in extra_destroyed:
            self.board.tiles[tile.i][tile.j] = None

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )

        return True

    def _activate_line_clear(self, tile) -> None:
        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        targets = self.board.get_line_clear_targets(tile)
        all_destroyed = [tile] + targets

        self.score += len(all_destroyed) * 50

        for t in all_destroyed:
            self.board.tiles[t.i][t.j] = None

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )

    def _activate_bomb(self, tile) -> None:
        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        targets = self.board.get_bomb_targets(tile)
        all_destroyed = [tile] + targets

        self.score += len(all_destroyed) * 50

        for t in all_destroyed:
            self.board.tiles[t.i][t.j] = None

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )
