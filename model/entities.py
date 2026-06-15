from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Player:
    id: int
    color: str
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


@dataclass
class Cell:
    x: int
    y: int
    player: Player | None = None
    neighbors: list["Cell"] = field(default_factory=list)
    is_dead_mark: bool = False
    is_blank: bool = True

    #dat quan co vao o
    def set_stone(self, player: Player) -> None:
        pass
    def clear_stone(self) -> None:
        pass


@dataclass
class Move:
    player: Player
    x: int | None = None
    y: int | None = None
    is_pass: bool = False

    def get_sgf_string(self) -> str:
        pass


