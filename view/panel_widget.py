from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from core.constant import Status, StoneColor


class PanelWidget(QWidget):
    pass_signal = pyqtSignal()
    resign_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    done_cleaning_signal = pyqtSignal()
    menu_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("panel_widget")
        self.setMinimumWidth(220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.turn_label = QLabel("Turn: -")
        self.status_label = QLabel("Status: -")
        self.winner_label = QLabel("")

        self.pass_button = QPushButton("Pass")
        self.resign_button = QPushButton("Resign")
        self.pause_button = QPushButton("Pause")
        self.done_cleaning_button = QPushButton("Done cleaning")
        self.menu_button = QPushButton("Menu")

        for button in (
            self.pass_button,
            self.resign_button,
            self.pause_button,
            self.done_cleaning_button,
            self.menu_button,
        ):
            button.setMinimumHeight(32)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)
        action_row.addWidget(self.pass_button)
        action_row.addWidget(self.resign_button)
        action_row.addWidget(self.menu_button)

        control_row = QHBoxLayout()
        control_row.setSpacing(10)
        control_row.addWidget(self.pause_button)
        control_row.addWidget(self.done_cleaning_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(self.turn_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.winner_label)
        layout.addLayout(action_row)
        layout.addLayout(control_row)
        layout.addStretch()

        self.pass_button.clicked.connect(self.pass_signal.emit)
        self.resign_button.clicked.connect(self.resign_signal.emit)
        self.pause_button.clicked.connect(self.pause_signal.emit)
        self.done_cleaning_button.clicked.connect(self.done_cleaning_signal.emit)
        self.menu_button.clicked.connect(self.menu_signal.emit)

    def update_turn_display(self, player_color: StoneColor, status: Status = Status.IDLE, winner_color: StoneColor = StoneColor.EMPTY) -> None:
        self.turn_label.setText(f"Turn: {player_color.name}")
        self.status_label.setText(f"Status: {status.name if isinstance(status, Status) else status}")
        if winner_color != StoneColor.EMPTY:
            self.winner_label.setText(f"Winner: {winner_color.name}")
        else:
            self.winner_label.setText("")
