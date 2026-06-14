from ..model.board_logic import board_logic
from ..model.rules import rules
from .mock import MockMainWindow

class game_controller:
    def __init__(self):
        self.mode = 1
        self.game_mode = "PVP"

    def new_game_start(self):
        pass

    def start_previous_match():
        pass
    def end_game():
        pass


class match_controller:
    def __init__(self, gamemode, main_window, rules, board_logic):
        self.gamemode = gamemode
        self.status = "PLAYING"

    def pvp_mode_start():
        pass
    def pve_mode_start():
        pass
    def end_match():
        pass
    def handle_click(x: int, y: int):
        pass
    def handle_pass():
        pass
    def handle_resign():
        pass





