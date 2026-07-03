from __future__ import annotations

from typing import TYPE_CHECKING

from ai.bot_algorithm import choose_best_move
from core.constant import StoneColor
from model.entities import Player

try:
    from PyQt6.QtCore import QObject, pyqtSignal
except ModuleNotFoundError:
    class _FallbackSignal:
        def __init__(self):
            self._slots = []

        def connect(self, slot):
            self._slots.append(slot)

        def emit(self, *args, **kwargs):
            for slot in self._slots:
                slot(*args, **kwargs)

    class _FallbackSignalDescriptor:
        def __set_name__(self, owner, name):
            self.name = f"_{name}"

        def __get__(self, instance, owner):
            if instance is None:
                return self
            if not hasattr(instance, self.name):
                setattr(instance, self.name, _FallbackSignal())
            return getattr(instance, self.name)

    def pyqtSignal(*_args, **_kwargs):
        return _FallbackSignalDescriptor()

    class QObject:
        def __init__(self, parent=None):
            self.parent = parent

        def moveToThread(self, thread):
            self.thread = thread

        def deleteLater(self):
            pass

if TYPE_CHECKING:
    from model.board_logic import BoardLogic

class BotAI(Player):
    """Basic Bot AI."""

    def select_move(self,board_logic: BoardLogic,) -> tuple[int, int] | None:
        return choose_best_move(board_logic)
    
class BotWorker(QObject):
    move_selected_signal = pyqtSignal(object)

    def __init__(self, parent=None, bot: BotAI = None, board_logic: BoardLogic = None):
        super().__init__(parent)
        self.bot = bot
        self.board_logic = board_logic
    def run(self):
        move = self.bot.select_move(board_logic=self.board_logic)
        self.move_selected_signal.emit(move)
