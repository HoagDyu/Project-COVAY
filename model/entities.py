from __future__ import annotations
from dataclasses import dataclass, field
from ..core.constant import StoneColor
from enum import Enum

@dataclass
class Player:
    color: StoneColor 
    territory: int = 0
    prisoner: int = 0
    komi: float = 0.0
    score: float = 0.0

    def add_territory(self, n: int) -> None:
        pass

    def add_prisoner(self, n: int) -> None:
        pass

    def add_point(self, n: float) -> None:
        pass

    def get_score(self) -> float:
        pass

    def set_player_color(self, color: StoneColor) -> None:
        self.color = color


@dataclass
class Cell:
    x: int
    y: int
    color: StoneColor = StoneColor.EMPTY #set kiểu dữ liệu là StoneColor và giá trị lúc khởi tạo là Empty
    neighbors: list["Cell"] = field(default_factory=list)
    is_dead_mark: bool = False
    is_blank: bool = True

    def set_stone_color(self, player: Player) -> None:
        pass

    def clear_stone(self) -> None:
        pass

    def get_cell_color(self):
        return self.color

@dataclass
class CellGroup:
    group: list["Cell"]
    liberties: int
    
    def add_cell(self, cell) -> None:
        self.group.append(cell)
    def update_liberties(self, ki: int) -> None:
        self.liberties = ki

@dataclass
class Move:
    player: Player
    x: int | None = None
    y: int | None = None
    is_pass: bool = False

    def get_sgf_string(self) -> str:
        pass


