from __future__ import annotations

from .entities import Move


class Rules:
    def is_valid_ip_place(self, move: Move, board: "BoardLogic") -> bool:
        pass

    def is_valid_place(self, move: Move, board: "BoardLogic") -> bool:
        pass

    def suicide(self, move: Move, board: "BoardLogic") -> bool:
        pass

    def ko(self, move: Move, board: "BoardLogic") -> bool:
        pass


rules = Rules
