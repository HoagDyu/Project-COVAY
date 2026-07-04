from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from view.board_widget import BoardWidget
from view.panel_widget import PanelWidget


class MatchScreen(QWidget):
    def __init__(self, board_size: int = 19):
        super().__init__()
        self.board_size = board_size

        self.board_widget = BoardWidget(board_size=board_size)
        self.panel_widget = PanelWidget()

        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.board_widget)
        layout.addSpacing(30)
        layout.addWidget(self.panel_widget, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch(1)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

