from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.constant import StoneColor


class MenuWidget(QWidget):
    pvp_start_signal = pyqtSignal()
    pve_start_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("menu_widget")

        title = QLabel("Go Game")
        title.setObjectName("menu_title")

        self.size_combo = QComboBox()
        for size in (9, 13, 19):
            self.size_combo.addItem(f"{size} x {size}", size)
        self.size_combo.setCurrentIndex(2)

        self.bot_color_combo = QComboBox()
        self.bot_color_combo.addItem("Bot plays White", StoneColor.WHITE)
        self.bot_color_combo.addItem("Bot plays Black", StoneColor.BLACK)

        form = QFormLayout()
        form.addRow("Board size", self.size_combo)
        form.addRow("Bot color", self.bot_color_combo)

        self.btn_pvp = QPushButton("Player vs Player")
        self.btn_pve = QPushButton("Player vs Bot")
        self.btn_exit = QPushButton("Exit")

        button_row = QHBoxLayout()
        button_row.addWidget(self.btn_pvp)
        button_row.addWidget(self.btn_pve)
        button_row.addWidget(self.btn_exit)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(button_row)
        layout.addStretch()

        self.btn_pvp.clicked.connect(self.pvp_start_signal.emit)
        self.btn_pve.clicked.connect(self.pve_start_signal.emit)

    def get_size(self) -> int:
        return int(self.size_combo.currentData())

    def get_bot(self) -> tuple[bool, StoneColor]:
        return True, self.bot_color_combo.currentData()
