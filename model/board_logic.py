from __future__ import annotations

from collections.abc import Iterable

from .entities import Cell, Move, Player

class Board:
    def __init__(self, rows = 19, cols = 19):
        self.rows = rows
        self.cols = cols
        self.board = []
        for x in range(rows):
            row = []
            for y in range(cols):
                cell = Cell(x, y)
                row.append(cell)
            self.board.append(row)

    #dieu kien ham place_stone:
    #1. cell phai trong board, kiem tra vi tri x, y co hop le hay khong
    #2. cell không được nằm cùng một ô với một quân cờ của đối thủ
    #3. ăn quân: check xung quanh có hết khí không, nếu hết khí thì xóa quân bị ăn
    #4. ktra nước đi tự tử: Sau khi ăn,  nếu quân mình đặt không có khí -> tự tử -> không hợp lệ -> báo lỗi
    
    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.board[x][y]
        return None

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols 

    def is_empty_cell(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        return cell is not None and cell.player is None


class BoardLogic:
    def __init__(self, size: int = 19):
        self.board = Board(size, size)
        

    def process_move(self, x: int, y: int) -> list[tuple[int, int]]:
        pass

    def _place_stone(self, move: Move) -> None:
        pass

    def _get_captured_groups(self, x: int, y: int) -> list[list[Cell]]:
        pass

    def _remove_captured_groups(self, groups: list[list[Cell]]) -> list[tuple[int, int]]:
        pass

    def process_pass(self) -> str:
        pass

    def pass_turn(self) -> None:
        pass

    def get_liberties(self, x: int, y: int, player: Player | None = None) -> int:
        pass

    def get_group(self, x: int, y: int) -> list[Cell]:
        pass

    def group_liberties(self, group: list[Cell]) -> int:
        pass

    def process_remove_dead_group(self, x: int, y: int) -> list[tuple[int, int]]:
        pass

    def remove_dead_group(self, x: int, y: int) -> int:
        pass

    def process_end_match(self) -> None:
        pass

    def calculate_all_territory(self) -> list[float]:
        pass

    def get_current_player(self) -> Player:
        pass


