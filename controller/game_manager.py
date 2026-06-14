from model.board_logic import BoardLogic


class GameController:
    def __init__(self, main_window):
        pass

    def game_start(self, gamemode: str):
        pass

    def read_history_log(self):
        pass

    def end_game(self) -> None:
        pass


class MatchController:
    def __init__(self, gamemode: str, status: str):
        pass

    def pvp_mode_start(self) -> None:
        pass

    def pve_mode_start(self) -> None:
        pass

    def end_match(self) -> None:
        pass

    def handle_click(self, x: int, y: int):
        pass

    def handle_pass(self):
        pass

    def handle_resign(self) -> None:
        pass


class game_controller(GameController):
    pass


class match_controller(MatchController):
    pass
