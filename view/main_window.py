from PyQt6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from view.match_screen import MatchScreen
from view.menu_widget import MenuWidget


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Go Game")
        self.resize(1040, 820)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_widget = MenuWidget()
        self.menu_view = self.menu_widget
        self.match_screen: MatchScreen | None = None
        self.board_widget = None
        self.panel_widget = None

        self.menu_widget.btn_exit.clicked.connect(self.close)
        self.menu_widget.pvp_start_signal.connect(self.switch_to_match_screen)
        self.menu_widget.pve_start_signal.connect(self.switch_to_match_screen)
        self.stack.addWidget(self.menu_widget)
        self.switch_to_menu_screen()

    def switch_to_menu_screen(self) -> None:
        self.stack.setCurrentWidget(self.menu_widget)

    def switch_to_match_screen(self, board_size: int | None = None) -> None:
        if board_size is None:
            board_size = self.menu_widget.get_size()

        if self.match_screen is not None:
            self.stack.removeWidget(self.match_screen)
            self.match_screen.deleteLater()

        self.match_screen = MatchScreen(board_size=board_size)
        self.board_widget = self.match_screen.board_widget
        self.panel_widget = self.match_screen.panel_widget

        self.stack.addWidget(self.match_screen)
        self.stack.setCurrentWidget(self.match_screen)

    def show_error(self, message: str) -> None:
        QMessageBox.warning(self, "Invalid move", message)

    def show_message(self, message: str) -> None:
        QMessageBox.information(self, "Go Game", message)
