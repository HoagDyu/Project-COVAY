from __future__ import annotations

from collections.abc import Iterable

from .entities import Cell, Move, Player


class BoardLogic:
    def __init__(self, size: int = 19):
        pass

    def process_move(self, x: int, y: int) -> bool:
        pass

    def _place_stone(self, move: Move) -> None:
        pass

    def _get_captured_groups(self, x: int, y: int) -> list[list[Cell]]:
        pass

    def _remove_captured_groups(self, groups: list[list[Cell]]) -> list[tuple[int, int]]:
        pass

    def process_pass(self) -> bool:
        pass

    def pass_turn(self) -> None:
        pass

    def get_liberties(self, x: int, y: int, player: Player | None = None) -> int:
        pass

    def get_group(self, x: int, y: int) -> list[Cell]:
        pass

    def group_liberties(self, group: list[Cell]) -> int:
        pass

    def process_remove_dead_group(self, x: int, y: int) -> bool:
        pass

    def remove_dead_group(self, x: int, y: int) -> int:
        pass

    def process_end_match(self) -> None:
        pass

    def calculate_all_territory(self) -> list[float]:
        pass

    def get_current_player(self) -> Player:
        pass
