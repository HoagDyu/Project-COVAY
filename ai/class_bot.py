from __future__ import annotations

from typing import TYPE_CHECKING

from bot_algorithm import choose_best_move
from core.constant import StoneColor
from model.entities import Player

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from model.board_logic import BoardLogic

class BotAI(Player):
    """Basic Bot AI."""

    def select_move(self, board_logic: BoardLogic) -> tuple[int, int] | None:
        return choose_best_move(board_logic=board_logic, bot=self)
    
class BotWorker(QObject):
    move_selected_signal = pyqtSignal(object)

    def __init__(self, parent=None,bot_color: StoneColor = StoneColor.EMPTY,  board_logic: BoardLogic = None):
        super().__init__(parent)
        self.bot = BotAI(color= bot_color)
        self.board_logic = board_logic
    def run(self):
        move = self.bot.select_move(board_logic=self.board_logic)
        self.move_selected_signal.emit(move)
