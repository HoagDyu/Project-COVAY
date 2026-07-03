from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
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
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        title = QLabel("Go Game")
        title.setObjectName("menu_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.size_combo = QComboBox()
        for size in (9, 13, 19):
            self.size_combo.addItem(f"{size} x {size}", size)
        self.size_combo.setCurrentIndex(2)

        self.bot_color_combo = QComboBox()
        self.bot_color_combo.addItem("Choose color for Bot", StoneColor.EMPTY)
        self.bot_color_combo.addItem("Bot plays White", StoneColor.WHITE)
        self.bot_color_combo.addItem("Bot plays Black", StoneColor.BLACK)

        form = QFormLayout()
        form.setSpacing(12)
        form.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)
        form.addRow("Board size", self.size_combo)
        form.addRow("Bot color", self.bot_color_combo)

        self.btn_pvp = QPushButton("Player vs Player")
        self.btn_pve = QPushButton("Player vs Bot")
        self.btn_exit = QPushButton("Exit")

        for button in (self.btn_pvp, self.btn_pve, self.btn_exit):
            button.setMinimumHeight(40)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        for combo in (self.size_combo, self.bot_color_combo):
            combo.setMinimumHeight(32)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)
        button_row.addWidget(self.btn_pvp)
        button_row.addWidget(self.btn_pve)
        button_row.addWidget(self.btn_exit)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(24)
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(button_row)
        layout.addStretch(2)

        self.btn_pvp.clicked.connect(self.pvp_start_signal.emit)
        self.btn_pve.clicked.connect(self.pve_start_signal.emit)

    def get_size(self) -> int:
        return int(self.size_combo.currentData())

    def get_bot(self) -> tuple[bool, StoneColor]:
        bot = True
        if self.bot_color_combo.currentData() == StoneColor.EMPTY:
            bot = False
        return bot, self.bot_color_combo.currentData()
