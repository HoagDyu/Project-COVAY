from ..model.board_logic import BoardLogic
from ..model.rules import Rules
from .mock import MockMainWindow

class GameController:
    def __init__(self, main_window):
        self.view = main_window
        self.current_match = None

        self.view.menu_view.pvp_start_signal.connect(lambda: self.game_start("PVP"))
        self.view.menu_view.pve_start_signal.connect(lambda: self.game_start("PVE"))

    def game_start(self,game_mode):
        self.board_logic = BoardLogic()
        self.rules = Rules()
        self.game_mode = game_mode

        self.current_match = MatchController(
            view=self.view,
            game_mode=self.game_mode,
            board_logic=self.board_logic,
            rules=self.rules
        )


    def end_game():
        pass


class MatchController:
    def __init__(self, board_logic, rules, view, game_mode):
        self.view = view
        self.game_mode = game_mode
        self.board_logic = board_logic
        self.rules = rules

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
            
    def pvp_match_start(self):
        pass

    def pve_match_start(self):
        pass

    def end_match():
        pass
    def handle_click(x: int, y: int):
        pass
    def handle_pass():
        pass
    def handle_resign():
        pass
    def handle_pause():
        pass
    def handle_undo():
        pass
    def handle_forward():
        pass





