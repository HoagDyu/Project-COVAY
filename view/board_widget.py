from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QGridLayout, QWidget

from view.cell_widget import CellWidget


class BoardWidget(QWidget):
    clicked_signal = pyqtSignal(int, int)

    def __init__(self, board_size: int, parent=None):
        super().__init__(parent)
        self.board_size = board_size
        self.cells: dict[tuple[int, int], CellWidget] = {}
        self._get_cell_color = None
        self._is_dead_cell = None

        self.setStyleSheet("background-color: #DCB35C;")
        self.init_board()

    def init_board(self) -> None:
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = CellWidget(row, col)
                cell.clicked_pos.connect(self.handle_cell_click)
                self.layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

    def handle_cell_click(self, row: int, col: int) -> None:
        self.clicked_signal.emit(row, col)

    def set_data_accessors(self, cell_getter, dead_getter) -> None:
        self._get_cell_color = cell_getter
        self._is_dead_cell = dead_getter

    def sync_board(self, matrix_2d) -> None:
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.cells[(row, col)].set_state(matrix_2d[row][col])

    def update(self) -> None:
        if self._get_cell_color is not None:
            for row in range(self.board_size):
                for col in range(self.board_size):
                    color = self._get_cell_color(row, col)
                    self.cells[(row, col)].set_state(color.value)
        super().update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine))

        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = self.cells[(row, col)]
                center_x = cell.x() + cell.width() // 2
                center_y = cell.y() + cell.height() // 2

                if col < self.board_size - 1:
                    next_cell = self.cells[(row, col + 1)]
                    painter.drawLine(
                        center_x,
                        center_y,
                        next_cell.x() + next_cell.width() // 2,
                        center_y,
                    )

                if row < self.board_size - 1:
                    next_cell = self.cells[(row + 1, col)]
                    painter.drawLine(
                        center_x,
                        center_y,
                        center_x,
                        next_cell.y() + next_cell.height() // 2,
                    )
