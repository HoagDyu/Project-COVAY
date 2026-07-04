from __future__ import annotations

from typing import TYPE_CHECKING
from PyQt6.QtCore import QThread

from core.constant import Status, StoneColor, GameMode
from model.board_logic import BoardLogic
from ai.class_bot import BotWorker

if TYPE_CHECKING:
    from view.main_window import MainWindow
class GameController:
    def __init__(self, main_window: MainWindow):
        self.view = main_window
        self.current_match = None

        self.view.menu_view.pvp_start_signal.connect(lambda: self.game_start(GameMode.PVP))
        self.view.menu_view.pve_start_signal.connect(lambda: self.game_start(GameMode.PVE))

    def game_start(self,game_mode: GameMode):
        self.game_mode = game_mode
        size = self.view.menu_widget.get_size()
        bot, bot_color = self.view.menu_widget.get_bot()
        time_seconds = self.view.menu_widget.get_time() * 60
        print("da chay")

        self.current_match = MatchController(
            view=self.view,
            game_mode=self.game_mode,
            size=size,
            bot=bot,
            bot_color=bot_color,
            time_seconds=time_seconds,
        )

class MatchController:
    def __init__(
        self,
        view: MainWindow,
        game_mode: GameMode,
        size: int,
        bot: bool = False,
        bot_color: StoneColor = StoneColor.EMPTY,
        time_seconds: int = 300,
    ):
        self.view = view
        self.game_mode = game_mode
        self.status = Status.IDLE
        self.winner: StoneColor
        self.has_bot = bot
        self.bot_color = bot_color
        self.thread = QThread()
        self.board_logic = BoardLogic(size=size, has_bot=bot, bot_color=bot_color,game_mode=game_mode)
        self.bot = self.board_logic.get_bot()

        cell_getter = self.board_logic.board.get_cell_color
        dead_getter = self.board_logic.board.is_dead_cell

        self.view.board_widget.set_data_accessors(cell_getter, dead_getter)

        self.view.board_widget.clicked_signal.connect(self.handle_click)
        self.view.panel_widget.resign_signal.connect(self.handle_resign)
        self.view.panel_widget.pass_signal.connect(self.handle_pass)
        self.view.panel_widget.pause_signal.connect(self.handle_pause)
        self.view.panel_widget.done_cleaning_signal.connect(self.end_match)
        self.view.panel_widget.menu_signal.connect(self.handle_menu)
        self.view.panel_widget.timeout_signal.connect(self.handle_timeout)
        self.view.panel_widget.set_clocks(time_seconds)

        if game_mode == GameMode.PVP:
            self.pvp_match_start()
        elif game_mode == GameMode.PVE:
            self.pve_match_start()

    def handle_bot_turn(self, move):
        if move is None:
            self.board_logic.process_pass()
            print("pass")
        else:
            x,y = move
            is_valid = self.board_logic.process_move(x=x,y=y)
            print(f"{x},{y}")
            if not is_valid:
                self.board_logic.process_pass()

        if self.board_logic.is_game_over:
            self.status = Status.CLEANING
        else:
            self.status = Status.HUMAN_TURN
        self.switch_turn()
        if self.status != Status.DONE:
            self.update_board()

    def start_bot_thread(self):
        self.bot_thread = QThread()
        self.bot_worker = BotWorker(bot_color = self.bot_color, board_logic=self.board_logic)

        self.bot_worker.moveToThread(self.bot_thread)

        self.bot_thread.started.connect(self.bot_worker.run)
        self.bot_worker.move_selected_signal.connect(self.handle_bot_turn)
        self.bot_worker.move_selected_signal.connect(self.bot_thread.quit)
        self.bot_thread.finished.connect(self.bot_worker.deleteLater)
        self.bot_thread.finished.connect(self.bot_thread.deleteLater)

        self.bot_thread.start()

    def update_board(self, winner_color: StoneColor = StoneColor.EMPTY):
        self.view.board_widget.update()
        self.view.panel_widget.update_prisoners(
            black_prisoners=self.board_logic.player_1.prisoner,
            white_prisoners=self.board_logic.player_2.prisoner,
        )
        next_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_turn_display(player_color = next_player_color, status = self.status, winner_color = winner_color)

    def pvp_match_start(self):
        self.status = Status.PLAYING
        first_player_color = self.board_logic.get_current_player().color
        self.view.panel_widget.update_prisoners(
            black_prisoners=self.board_logic.player_1.prisoner,
            white_prisoners=self.board_logic.player_2.prisoner,
        )
        self.view.panel_widget.update_turn_display(player_color = first_player_color, status = self.status)
        self.view.board_widget.update()

    def switch_turn(self):
        self.board_logic.switch_turn()
        current_player_color = self.board_logic.get_current_player().color
        match self.game_mode:
            case GameMode.PVE:
                if self.has_bot and self.board_logic.is_game_over:
                    print("thoa")
                    self.end_match()
                elif self.has_bot and current_player_color == self.bot_color:
                    self.status = Status.BOT_TURN
                    self.start_bot_thread()
                else:
                    self.status = Status.HUMAN_TURN
            case GameMode.PVP:
                if self.board_logic.is_game_over:
                    self.status = Status.CLEANING
                else:
                    self.status = Status.PLAYING

    def pve_match_start(self):
        print("chay bot")
        if self.has_bot:
            if self.bot_color == StoneColor.BLACK:
                self.status = Status.BOT_TURN
                self.view.panel_widget.update_prisoners(
                    black_prisoners=self.board_logic.player_1.prisoner,
                    white_prisoners=self.board_logic.player_2.prisoner,
                )
                self.view.panel_widget.update_turn_display(player_color = StoneColor.BLACK, status = self.status)
                self.view.board_widget.update()
                self.start_bot_thread()
                return
            elif self.bot_color == StoneColor.WHITE:
                self.status = Status.HUMAN_TURN
        self.view.panel_widget.update_prisoners(
            black_prisoners=self.board_logic.player_1.prisoner,
            white_prisoners=self.board_logic.player_2.prisoner,
        )
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
                    self.switch_turn()
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
        match self.status:
            case Status.PAUSE | Status.BOT_TURN | Status.DONE:
                pass
            case Status.PLAYING | Status.HUMAN_TURN | Status.CLEANING:
                self.board_logic.process_pass()
                self.switch_turn()
                if self.status != Status.DONE:
                    self.update_board()

    def handle_resign(self):
        match self.status:
            case Status.PAUSE | Status.BOT_TURN | Status.DONE:
                pass
            case Status.PLAYING | Status.HUMAN_TURN | Status.CLEANING:
                self.status = Status.DONE
                self.winner = self.board_logic.resign()
                self.update_board(winner_color=self.winner)

    def handle_pause(self):
        match self.status:
            case Status.PAUSE:
                if self.game_mode == GameMode.PVP:
                    self.status = Status.PLAYING
                elif self.game_mode == GameMode.PVE and self.board_logic.get_current_player().color != self.bot_color:
                    self.status = Status.HUMAN_TURN
                else:
                    self.status = Status.BOT_TURN
                self.update_board()
            case Status.BOT_TURN | Status.DONE:
                pass
            case Status.PLAYING | Status.HUMAN_TURN | Status.CLEANING:
                self.status = Status.PAUSE
                self.update_board()

    def handle_menu(self):
        self.view.switch_to_menu_screen()

    def handle_timeout(self, loser_color: StoneColor):
        if loser_color == StoneColor.BLACK:
            self.winner = StoneColor.WHITE
        elif loser_color == StoneColor.WHITE:
            self.winner = StoneColor.BLACK
        else:
            return
        self.board_logic.is_game_over = True
        self.status = Status.DONE
        self.update_board(winner_color=self.winner)

    
