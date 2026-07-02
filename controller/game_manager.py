from __future__ import annotations

from typing import TYPE_CHECKING

from core.constant import Status, StoneColor
from model.board_logic import BoardLogic

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

        self.current_match = MatchController(
            view=self.view,
            game_mode=self.game_mode
        )

    def end_game():
        pass


class MatchController:
    def __init__(self, view: MainWindow, game_mode: str, bot=None):
        self.view = view
        self.game_mode = game_mode
        self.board_logic = BoardLogic()
        self.status = Status.IDLE
        self.winner: StoneColor

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
            
    def update_board(self, winner_color: StoneColor = StoneColor.EMPTY):
        self.view.board_widget.update()
        next_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_turn_display(player_color = next_player_color, status = self.status, winner_color = winner_color)


    def pvp_match_start(self):
        self.status = Status.PLAYING
        first_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_turn_display(player_color = first_player_color, status = self.status)
        self.view.board_widget.update()


    def pve_match_start(self):
        pass

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

    



