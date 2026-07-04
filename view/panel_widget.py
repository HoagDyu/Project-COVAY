import os

from PyQt6 import uic
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget,QPushButton, QLCDNumber


from core.constant import Status, StoneColor


class PanelWidget(QWidget):
    btn_pass: QPushButton
    btn_resign: QPushButton
    bt_pause: QPushButton
    btn_done_cleaning: QPushButton
    btn_menu: QPushButton
    black_number: QLCDNumber
    white_number: QLCDNumber
    black_prisoner_number: QLCDNumber
    white_prisoner_number: QLCDNumber
    black_ava: QPushButton
    white_ava: QPushButton

    pass_signal = pyqtSignal()
    resign_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    done_cleaning_signal = pyqtSignal()
    menu_signal = pyqtSignal()
    timeout_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__),"ui", "panel.ui")
        uic.loadUi(ui_path, self)

        self.remaining_time = {
            StoneColor.BLACK: 0,
            StoneColor.WHITE: 0,
        }
        self.active_clock_color = StoneColor.EMPTY
        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self._tick_clock)

        self.btn_pass.clicked.connect(self.pass_signal.emit)
        self.btn_resign.clicked.connect(self.resign_signal.emit)
        self.bt_pause.clicked.connect(self.pause_signal.emit)
        self.btn_done_cleaning.clicked.connect(self.done_cleaning_signal.emit)
        self.btn_menu.clicked.connect(self.menu_signal.emit)

        self.set_up_color()

        self._update_clock_labels()
        self.update_prisoners(0, 0)

    def set_up_color(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.setStyleSheet("""
            QWidget#Form {
                background-color: #1e1e1e;
                border: 3px solid #555;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #595959;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                max-height: 40px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #0D47A1; }

            QLCDNumber {
                background-color: black;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                max-height: 30px;
                max-width: 70px;
            }
        """)

        self.white_ava.setStyleSheet("""
            background-color: black; 
            color: white; 
            border-radius: 6px;
            padding: 8px; 
            min-height: 60px;
            min-width: 90px;
        """)
        self.black_ava.setStyleSheet("""
            background-color: white; 
            color: black; 
            border: 1px solid #ccc;
            border-radius: 6px; 
            padding: 8px;  
            min-height: 60px;
            min-width: 90px;
        """)

        self.btn_pass.setStyleSheet("""
            background-color: #595959;
            color: white;
            border-radius: 6px;
            padding: 6px 10px;
            font-weight: bold;
            max-width: 70px;
            max-height: 32px;
        """)
        self.gridLayout_2.setContentsMargins(15, 15, 15, 15)
        self.gridLayout_5.setAlignment(self.btn_pass, Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.setColumnMinimumWidth(0, 90)
        self.gridLayout_5.setColumnMinimumWidth(2, 90)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 0)   
        self.gridLayout_5.setColumnStretch(2, 1)
        self.gridLayout_5.setSpacing(15)

        for w in [self.black_number, self.white_number,
                self.black_prisoner_number, self.white_prisoner_number,
                self.black_ava, self.white_ava]:
            self.gridLayout_5.setAlignment(w, Qt.AlignmentFlag.AlignCenter)


    def update_turn_display(
        self,
        player_color: StoneColor,
        status: Status = Status.IDLE,
        winner_color: StoneColor = StoneColor.EMPTY,
    ) -> None:
        self.turn.setText(f"Turn: {player_color.name}")
        self.status_lab.setText(f"Status: {status.name if isinstance(status, Status) else status}")
        if winner_color != StoneColor.EMPTY:
            self.winner_lab.setText(f"Winner: {winner_color.name}")
        else:
            self.winner_lab.setText("Winner:")
        self._sync_clock_with_turn(player_color, status)

    def set_clocks(self, initial_seconds: int) -> None:
        initial_seconds = max(0, int(initial_seconds))
        self.remaining_time[StoneColor.BLACK] = initial_seconds
        self.remaining_time[StoneColor.WHITE] = initial_seconds
        self.active_clock_color = StoneColor.EMPTY
        self.clock_timer.stop()
        self._update_clock_labels()

    def start_clock(self, player_color: StoneColor) -> None:
        if player_color not in (StoneColor.BLACK, StoneColor.WHITE):
            self.stop_clocks()
            return

        self.active_clock_color = player_color
        if self.remaining_time[player_color] <= 0:
            self.stop_clocks()
            self.timeout_signal.emit(player_color)
            return

        self.clock_timer.start()

    def stop_clocks(self) -> None:
        self.active_clock_color = StoneColor.EMPTY
        self.clock_timer.stop()

    def _sync_clock_with_turn(self, player_color: StoneColor, status: Status) -> None:
        if status in (Status.PLAYING, Status.HUMAN_TURN, Status.BOT_TURN):
            self.start_clock(player_color)
        else:
            self.stop_clocks()

    def _tick_clock(self) -> None:
        color = self.active_clock_color
        if color not in (StoneColor.BLACK, StoneColor.WHITE):
            self.stop_clocks()
            return

        self.remaining_time[color] = max(0, self.remaining_time[color] - 1)
        self._update_clock_labels()

        if self.remaining_time[color] == 0:
            self.stop_clocks()
            self.timeout_signal.emit(color)

    def _update_clock_labels(self) -> None:
        black_seconds = self.remaining_time[StoneColor.BLACK]
        white_seconds = self.remaining_time[StoneColor.WHITE]

        self.black_number.display(self._format_time(black_seconds))
        self.white_number.display(self._format_time(white_seconds))

    def update_prisoners(self, black_prisoners: int, white_prisoners: int) -> None:
        self.black_prisoner_number.display(max(0, int(black_prisoners)))
        self.white_prisoner_number.display(max(0, int(white_prisoners)))

    def _format_time(self, seconds: int) -> str:
        minutes, seconds = divmod(max(0, int(seconds)), 60)
        return f"{minutes:02d}:{seconds:02d}"
