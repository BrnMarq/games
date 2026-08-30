"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Board.
"""

from typing import List, Optional, Tuple, Any, Dict, Set

import pygame

import random

import settings
from src.Tile import Tile


class Board:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.matches: List[List[Tile]] = []
        self.tiles: List[List[Tile]] = []
        self._initialize_tiles()
        while not self.has_valid_move():
            self._initialize_tiles()

    def render(self, surface: pygame.Surface) -> None:
        for row in self.tiles:
            for tile in row:
                tile.render(surface, self.x, self.y)

    def _is_match_generated(self, i: int, j: int, color: int) -> bool:
        if (
            i >= 2
            and self.tiles[i - 1][j].color == color
            and self.tiles[i - 2][j].color == color
        ):
            return True

        return (
            j >= 2
            and self.tiles[i][j - 1].color == color
            and self.tiles[i][j - 2].color == color
        )

    def _initialize_tiles(self) -> None:
        self.tiles = [
            [None for _ in range(settings.BOARD_WIDTH)]
            for _ in range(settings.BOARD_HEIGHT)
        ]
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                color = random.randint(0, settings.NUM_COLORS - 1)
                while self._is_match_generated(i, j, color):
                    color = random.randint(0, settings.NUM_COLORS - 1)

                self.tiles[i][j] = Tile(i, j, color, settings.BASE_TILE_FRAME)

    def _calculate_match_rec(self, tile: Tile) -> Set[Tile]:
        if tile in self.in_stack:
            return []

        self.in_stack.add(tile)

        color_to_match = tile.color

        ## Check horizontal match
        h_match: List[Tile] = []

        # Check left
        if tile.j > 0:
            left = max(0, tile.j - 2)
            for j in range(tile.j - 1, left - 1, -1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        # Check right
        if tile.j < settings.BOARD_WIDTH - 1:
            right = min(settings.BOARD_WIDTH - 1, tile.j + 2)
            for j in range(tile.j + 1, right + 1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        ## Check vertical match
        v_match: List[Tile] = []

        # Check top
        if tile.i > 0:
            top = max(0, tile.i - 2)
            for i in range(tile.i - 1, top - 1, -1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        # Check bottom
        if tile.i < settings.BOARD_HEIGHT - 1:
            bottom = min(settings.BOARD_HEIGHT - 1, tile.i + 2)
            for i in range(tile.i + 1, bottom + 1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        match: List[Tile] = []

        if len(h_match) >= 2:
            for t in h_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(v_match) >= 2:
            for t in v_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(match) > 0:
            if tile not in self.in_match:
                self.in_match.add(tile)
                match.append(tile)

        for t in match:
            match += self._calculate_match_rec(t)

        self.in_stack.remove(tile)
        return match

    def calculate_matches_for(
        self, new_tiles: List[Tile]
    ) -> Optional[List[List[Tile]]]:
        self.in_match: Set[Tile] = set()
        self.in_stack: Set[Tile] = set()

        for tile in new_tiles:
            if tile in self.in_match:
                continue
            match = self._calculate_match_rec(tile)
            if len(match) > 0:
                self.matches.append(match)

        delattr(self, "in_match")
        delattr(self, "in_stack")

        return self.matches if len(self.matches) > 0 else None

    def remove_matches(self) -> None:
        for match in self.matches:
            for tile in match:
                if tile.powerup is None:
                    self.tiles[tile.i][tile.j] = None

        self.matches = []

    def get_line_clear_targets(self, tile: Tile) -> List[Tile]:
        targets = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = tile.i + di, tile.j + dj
            if 0 <= ni < settings.BOARD_HEIGHT and 0 <= nj < settings.BOARD_WIDTH:
                t = self.tiles[ni][nj]
                if t is not None:
                    targets.append(t)
        return targets

    def get_bomb_targets(self, tile: Tile) -> List[Tile]:
        targets = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = tile.i + di, tile.j + dj
                if 0 <= ni < settings.BOARD_HEIGHT and 0 <= nj < settings.BOARD_WIDTH:
                    t = self.tiles[ni][nj]
                    if t is not None:
                        targets.append(t)
        return targets

    def collect_cascade_targets(self, powerup_tiles: List[Tile]) -> List[Tile]:
        all_targets = []
        visited = set()
        queue = list(powerup_tiles)

        while queue:
            tile = queue.pop(0)
            if (tile.i, tile.j) in visited:
                continue
            visited.add((tile.i, tile.j))

            if tile.powerup == "line_clear":
                targets = self.get_line_clear_targets(tile)
            elif tile.powerup == "bomb":
                targets = self.get_bomb_targets(tile)
            else:
                continue

            for t in targets:
                if (t.i, t.j) not in visited:
                    all_targets.append(t)
                    if t.powerup is not None:
                        queue.append(t)

        return all_targets

    def get_falling_tiles(self) -> Tuple[Any, Dict[str, Any]]:
        # List of tweens to create
        tweens: Tuple[Tile, Dict[str, Any]] = []

        # for each column, go up tile by tile until we hit a space
        for j in range(settings.BOARD_WIDTH):
            space = False
            space_i = -1
            i = settings.BOARD_HEIGHT - 1

            while i >= 0:
                tile = self.tiles[i][j]

                # if our previous tile was a space
                if space:
                    # if the current tile is not a space
                    if tile is not None:
                        self.tiles[space_i][j] = tile
                        tile.i = space_i

                        # set its prior position to None
                        self.tiles[i][j] = None

                        tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))
                        space = False
                        i = space_i
                        space_i = -1
                elif tile is None:
                    space = True

                    if space_i == -1:
                        space_i = i

                i -= 1

        # create a replacement tiles at the top of the screen
        for j in range(settings.BOARD_WIDTH):
            for i in range(settings.BOARD_HEIGHT):
                tile = self.tiles[i][j]

                if tile is None:
                    tile = Tile(
                        i,
                        j,
                        random.randint(0, settings.NUM_COLORS - 1),
                        settings.BASE_TILE_FRAME,
                    )
                    tile.y -= settings.TILE_SIZE
                    self.tiles[i][j] = tile
                    tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))

        return tweens

    def _check_at(self, center_row, center_col):
        target_color = self.tiles[center_row][center_col].color

        horizontal_count = 1
        for offset in range(1, 3):
            col = center_col - offset
            if col < 0 or self.tiles[center_row][col].color != target_color:
                break
            horizontal_count += 1
        for offset in range(1, 3):
            col = center_col + offset
            if col >= settings.BOARD_WIDTH or self.tiles[center_row][col].color != target_color:
                break
            horizontal_count += 1
        if horizontal_count >= 3:
            return True

        vertical_count = 1
        for offset in range(1, 3):
            row = center_row - offset
            if row < 0 or self.tiles[row][center_col].color != target_color:
                break
            vertical_count += 1
        for offset in range(1, 3):
            row = center_row + offset
            if row >= settings.BOARD_HEIGHT or self.tiles[row][center_col].color != target_color:
                break
            vertical_count += 1
        return vertical_count >= 3

    def has_valid_move(self) -> bool:
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                if self.tiles[i][j].powerup is not None:
                    return True
                if j < settings.BOARD_WIDTH - 1:
                    self.tiles[i][j], self.tiles[i][j + 1] = self.tiles[i][j + 1], self.tiles[i][j]
                    if self._check_at(i, j) or self._check_at(i, j + 1):
                        self.tiles[i][j], self.tiles[i][j + 1] = self.tiles[i][j + 1], self.tiles[i][j]
                        return True
                    self.tiles[i][j], self.tiles[i][j + 1] = self.tiles[i][j + 1], self.tiles[i][j]
                if i < settings.BOARD_HEIGHT - 1:
                    self.tiles[i][j], self.tiles[i + 1][j] = self.tiles[i + 1][j], self.tiles[i][j]
                    if self._check_at(i, j) or self._check_at(i + 1, j):
                        self.tiles[i][j], self.tiles[i + 1][j] = self.tiles[i + 1][j], self.tiles[i][j]
                        return True
                    self.tiles[i][j], self.tiles[i + 1][j] = self.tiles[i + 1][j], self.tiles[i][j]
        return False
