from __future__ import annotations

from typing import TYPE_CHECKING

from core.constant import StoneColor
from .entities import Move

if TYPE_CHECKING:
    from .board_logic import Board, BoardLogic


class Rules:
    def __init__(self, board: "Board"):
        self.board = board

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.board.rows and 0 <= y < self.board.cols

    def is_empty_cell(self, x: int, y: int) -> bool:
        if self.is_valid_move(x, y):
            return self.board.get_cell(x, y).is_blank
        return False

    def is_dead_cell(self, x: int, y: int) -> bool:
        return self.board.get_cell(x, y).is_dead_mark

    def is_suicide(self, x: int, y: int, move: Move, board: "BoardLogic") -> bool:
        if move.is_pass or move.x is None or move.y is None:
            return False

        if not self.is_valid_move(x, y):
            return False

        own_color = move.player.color
        opponent_color = StoneColor.WHITE if own_color == StoneColor.BLACK else StoneColor.BLACK

        for neighbor in board.board.get_cell(x, y).neighbors:
            if neighbor.get_cell_color() == StoneColor.EMPTY:
                return False

        for neighbor in board.board.get_cell(x, y).neighbors:
            if neighbor.get_cell_color() == opponent_color:
                opponent_group = board.get_group(neighbor.x, neighbor.y)
                if board.board.group_liberties(opponent_group) == 1:
                    return False

        for neighbor in board.board.get_cell(x, y).neighbors:
            if neighbor.get_cell_color() == own_color:
                own_group = board.get_group(neighbor.x, neighbor.y)
                if board.board.group_liberties(own_group) > 1:
                    return False

        return True

    def is_ko(self, move: Move, board: "BoardLogic") -> bool:
        if move.is_pass or move.x is None or move.y is None:
            return False
        if len(board.move_history) < 2:
            return False

        previous_move = board.move_history[-2]
        if previous_move.is_pass or previous_move.x is None or previous_move.y is None:
            return False

        return move.x == previous_move.x and move.y == previous_move.y

    def is_gameover(self, board: "BoardLogic") -> bool:
        if board.game_over:
            return True
        if len(board.move_history) < 2:
            return False

        last_move = board.move_history[-1]
        second_last_move = board.move_history[-2]
        return last_move.is_pass and second_last_move.is_pass


rules = Rules
