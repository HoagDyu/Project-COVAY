from __future__ import annotations

from typing import TYPE_CHECKING

try:
    from PyQt6.QtCore import QThread
except ModuleNotFoundError:
    class _FallbackSignal:
        def __init__(self):
            self._slots = []

        def connect(self, slot):
            self._slots.append(slot)

        def emit(self, *args, **kwargs):
            for slot in list(self._slots):
                slot(*args, **kwargs)

    class QThread:
        def __init__(self):
            self.started = _FallbackSignal()
            self.finished = _FallbackSignal()

        def start(self):
            self.started.emit()

        def quit(self):
            self.finished.emit()

        def deleteLater(self):
            pass

from core.constant import Status, StoneColor
from model.board_logic import BoardLogic
from ai.class_bot import BotWorker

if TYPE_CHECKING:
    from view.main_window import MainWindow
class GameController:
    def __init__(self, main_window: MainWindow):
        self.view = main_window
        self.current_match = None

        self.view.menu_view.pvp_start_signal.connect(lambda: self.game_start("PVP"))
        self.view.menu_view.pve_start_signal.connect(lambda: self.game_start("PVE"))

    def game_start(self,game_mode: str):
        self.game_mode = game_mode
        size = self.view.menu_widget.get_size()
        bot, bot_color = self.view.menu_widget.get_bot()

        self.current_match = MatchController(
            view=self.view,
            game_mode=self.game_mode,
            size=size,
            bot=bot,
            bot_color = bot_color
        )

    def end_game():
        pass


class MatchController:
    def __init__(self, view: MainWindow, game_mode: str, size: int, bot=None, bot_color: StoneColor = StoneColor.EMPTY):
        self.view = view
        self.game_mode = game_mode
        self.status = Status.IDLE
        self.winner: StoneColor
        self.bot = bot
        self.bot_color = bot_color
        self.thread = QThread()
        self.board_logic = BoardLogic(size=size, bot=bot, bot_color=bot_color)

        cell_getter = self.board_logic.board.get_cell_color
        dead_getter = self.board_logic.board.is_dead_cell

        self.view.board_widget.set_data_accessors(cell_getter, dead_getter)

        self.view.board_widget.clicked_signal.connect(self.handle_click)
        self.view.panel_widget.resign_signal.connect(self.handle_resign)
        self.view.panel_widget.pass_signal.connect(self.handle_pass)
        self.view.panel_widget.pause_signal.connect(self.handle_pause)
        self.view.panel_widget.done_cleaning_signal.connect(self.end_match)

        if game_mode == "PVP":
            self.pvp_match_start()
        else:
            self.pve_match_start()

    def handle_bot_turn(self, move):
        if move is None:
            self.board_logic.process_pass()
        else:
            x,y = move
            self.board_logic.process_move(x=x,y=y)
        self.switch_turn()
        self.update_board()

    def start_bot_thread(self):
        self.bot_thread = QThread()
        self.bot_worker = BotWorker(bot=self.bot, board_logic=self.board_logic)

        self.bot_worker.moveToThread(self.bot_thread)

        self.bot_thread.started.connect(self.bot_worker.run)
        self.bot_worker.move_selected_signal.connect(self.handle_bot_turn)
        self.bot_worker.move_selected_signal.connect(self.bot_thread.quit)
        self.bot_thread.finished.connect(self.bot_worker.deleteLater)
        self.bot_thread.finished.connect(self.bot_thread.deleteLater)

        self.bot_thread.start()

    def update_board(self, winner_color: StoneColor = StoneColor.EMPTY):
        self.view.board_widget.update()
        next_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_turn_display(player_color = next_player_color, status = self.status, winner_color = winner_color)

    def pvp_match_start(self):
        self.status = Status.PLAYING
        first_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_turn_display(player_color = first_player_color, status = self.status)
        self.view.board_widget.update()

    def switch_turn(self):
        self.board_logic.switch_turn()
        current_player_color = self.board_logic.get_current_player().color
        if self.bot and current_player_color == self.bot_color:
            self.status = Status.BOT_TURN
            self.start_bot_thread()
        else:
            self.status = Status.HUMAN_TURN

    def pve_match_start(self):
        if self.bot:
            if self.bot_color == StoneColor.BLACK:
                self.status = Status.BOT_TURN
            elif self.bot_color == StoneColor.WHITE:
                self.status = Status.HUMAN_TURN
        self.view.panel_widget.update_turn_display(player_color = StoneColor.BLACK, status = self.status)
        self.view.board_widget.update()
        
    def end_match(self):
        self.status = Status.DONE
        self.winner = self.board_logic.process_end_match()
        self.update_board(winner_color=self.winner)

    def handle_click(self,x: int, y: int):
        match self.status:
            case Status.PLAYING | Status.HUMAN_TURN:
                is_valid = self.board_logic.process_move(x=x,y=y)
                if is_valid:
                    self.update_board()
                else:
                    self.view.show_error("invalid move")
            case Status.PAUSE | Status.BOT_TURN | Status.DONE:
                pass
            case Status.CLEANING:
                is_valid = self.board_logic.process_dead_group(x=x, y=y)
                if is_valid:
                    self.update_board()
        
    def handle_pass(self):
        self.board_logic.process_pass()
        if self.board_logic.is_game_over:
            self.status = Status.CLEANING
            self.update_board()

    def handle_resign(self):
        self.status = Status.DONE
        self.winner = self.board_logic.resign()
        self.update_board(winner_color=self.winner)

    def handle_pause(self):
        self.status = Status.PAUSE
        self.update_board()

    



