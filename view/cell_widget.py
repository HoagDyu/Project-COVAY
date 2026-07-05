from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QPushButton, QSizePolicy

from core.constant import StoneColor


class CellWidget(QPushButton):
    clicked_pos = pyqtSignal(int, int)

    def __init__(self, row: int, col: int, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.state = StoneColor.EMPTY.value

        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.clicked.connect(self.on_click)
        self.update_style()

    def set_state(self, state: int) -> None:
        self.state = state
        self.update_style()

    def update_style(self) -> None:
        diameter = max(1, min(self.width(), self.height()))
        margin = max(2, diameter // 12)
        radius = max(1, (diameter - margin * 2) // 2)

        if self.state == StoneColor.BLACK.value:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: black;
                    border-radius: {radius}px;
                    margin: {margin}px;
                }}
                """
            )
        elif self.state == StoneColor.WHITE.value:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: white;
                    border: 1px solid #333;
                    border-radius: {radius}px;
                    margin: {margin}px;
                }}
                """
            )
        else:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 0, 0, 0.2);
                    border-radius: {radius}px;
                    margin: {margin}px;
                }}
                """
            )

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.update_style()

    def on_click(self) -> None:
        self.clicked_pos.emit(self.row, self.col)
