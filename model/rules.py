<<<<<<< HEAD
# (Tùy chọn) Tách riêng luật Ko, cấm tự sát ra đây
=======
from __future__ import annotations

from .entities import Move
from .board_logic import BoardLogic


class Rules:
    def is_valid_to_place(self, move: Move, board: BoardLogic) -> bool:
        # Kiem tra move hop le: 1. move phai trong board, 2. cell tai move phai trong, 3. cell phai khong co quan co, 4. ktra suicide, 5. ktra ko, 6. co pass hay khong
        
        pass

    def is_suicide(self, move: Move, board: BoardLogic) -> bool:
        pass

    def is_ko(self, move: Move, board: BoardLogic) -> bool:
        pass


>>>>>>> master
