from __future__ import annotations

from .entities import Move, Cell, Player
from .board_logic import BoardLogic, Board


class Rules:
    def __init__(self, board: Board):
          self.board = board

    def is_valid_to_place(self, move: Move, board: BoardLogic) -> bool: #type: ignore
        # Kiem tra move hop le: 1. move phai trong board, 2. cell tai move phai trong, 3. cell phai khong co quan co, 4. ktra suicide, 5. ktra ko, 6. co pass hay khong
        pass

    def is_valid_move(self, x: int, y: int) -> bool:
            return 0 <= x < self.board.rows and 0 <= y < self.board.cols

    def is_empty_cell(self, x: int, y: int) -> bool:
            if self.is_valid_move(x, y):
                cell = self.board.get_cell(x, y)
                return cell.is_blank
            return False
    
    def is_dead_cell(self, x:int, y:int) -> bool:
            cell = self.board.get_cell(x, y)
            return cell.is_dead_mark

    def is_suicide(self, move: Move, board: BoardLogic) -> bool:
        pass

    def is_ko(self, move: Move, board: BoardLogic) -> bool:
        pass


