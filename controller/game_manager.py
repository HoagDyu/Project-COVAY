
from ..model.board_logic import BoardLogic
from .mock import MockMainWindow
from ..core.constant import Status

class GameController:
    def __init__(self, main_window: MockMainWindow):
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
    def __init__(self, view: MockMainWindow, game_mode: str, bot=None):
        self.view = view
        self.game_mode = game_mode
        self.board_logic = BoardLogic()
        self.status = Status.IDLE

        cell_getter = self.board_logic.board.get_cell_color
        dead_getter = self.board_logic.board.is_dead_cell

        self.view.board_widget.set_data_accessors(cell_getter, dead_getter)

        self.view.board_widget.clicked_signal.connect(self.handle_click)
        self.view.panel_widget.resign_signal.connect(self.handle_resign)
        self.view.panel_widget.pass_signal.connect(self.handle_pass)
        self.view.panel_widget.pause_signal.connect(self.handle_pause)
        self.view.panel_widget.undo_signal.connect(self.handle_undo)
        self.view.panel_widget.forward_signal.connect(self.handle_forward)

        if game_mode == "PVP":
            self.pvp_match_start()
        else:
            self.pve_match_start()
            
    def update_board(self):
        self.view.board_widget.update()
        next_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_turn_display(next_player_color)

    def pvp_match_start(self):
        self.status = "PLAYING" 
        first_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_turn_display(first_player_color)
        self.view.board_widget.update()


    def pve_match_start(self):
        pass

    def end_match():
        pass
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
        self.board_logic.pass_turn()
    def handle_resign(self):
        self.board_logic.resign()
    def handle_pause(self):
        self.status = Status.PAUSE

