import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter, QPen
from view.cell_widget import CellWidget


class BoardWidget(QWidget):
    # Gom tín hiệu: Phát ra một tín hiệu duy nhất kèm tọa độ (x, y) hay (row, col) cho Controller
    clicked_signal = pyqtSignal(int, int)

    def __init__(self, board_size: int, parent=None):
        super().__init__(parent)
        self.board_size = board_size
        self.cells = {} # Dictionary để lưu tham chiếu tới các CellWidget
        
        # Thiết lập giao diện tổng thể
        self.setStyleSheet("background-color: #DCB35C;") # Màu nền gỗ cho bàn cờ
        
        # Khởi tạo layout và bàn cờ
        self.init_board()

    def init_board(self):
        """Khởi tạo bàn cờ, tự động gán tọa độ cho từng ô"""
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0) # Đặt khoảng cách giữa các ô là 0
        
        # Tạo lưới (Ví dụ 19x19, 13x13, 9x9)
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Tạo CellWidget và tự động gán tọa độ
                cell = CellWidget(row, col)
                
                # Gom tín hiệu: Lắng nghe click từ ô con
                cell.clicked_pos.connect(self.handle_cell_click)
                
                # Thêm vào layout và lưu trữ
                self.layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

    def handle_cell_click(self, row, col):
        """Hàm nhận tín hiệu từ CellWidget và phát tiếp cho Controller"""
        # Trạm trung chuyển: Phát tín hiệu tổng ra bên ngoài
        self.clicked_signal.emit(row, col)

    def sync_board(self, matrix_2d):
        """Đồng bộ hóa: Nhận mảng 2D và cập nhật màu cho toàn bộ CellWidget"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                state = matrix_2d[row][col]
                self.cells[(row, col)].set_state(state)

    def paintEvent(self, event):
        """(Mở rộng thêm) Vẽ các đường kẻ lưới chuẩn của cờ vây cắt ngang các CellWidget"""
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        # Do các ô rỗng của CellWidget trong suốt (transparent), 
        # ta vẽ các đường thẳng kết nối tâm của chúng ở lớp nền (background)
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = self.cells[(row, col)]
                # Lấy tâm của từng ô
                center_x = cell.x() + cell.width() // 2
                center_y = cell.y() + cell.height() // 2

                # Vẽ đường kẻ ngang
                if col < self.board_size - 1:
                    next_cell = self.cells[(row, col + 1)]
                    painter.drawLine(center_x, center_y, next_cell.x() + next_cell.width() // 2, center_y)
                
                # Vẽ đường kẻ dọc
                if row < self.board_size - 1:
                    next_cell = self.cells[(row + 1, col)]
                    painter.drawLine(center_x, center_y, center_x, next_cell.y() + next_cell.height() // 2)


# =======================================================
# 3. CODE TEST (Giả lập Controller điều khiển BoardWidget)
# =======================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Giả sử chọn bàn cờ nhỏ 9x9 để dễ nhìn
    SIZE = 13
    
    # Tạo BoardWidget
    board = BoardWidget(board_size=SIZE)
    board.setWindowTitle("Bàn cờ vây - BoardWidget")
    
    # Giả lập 1 ma trận 2D phía Controller (0: Rỗng, 1: Đen, 2: Trắng)
    # Khởi tạo ma trận toàn số 0
    game_matrix = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    
    # Lượt chơi hiện tại (1 là Đen, 2 là Trắng)
    current_turn = [1] 

    def on_board_clicked(row, col):
        """Logic Controller khi nhận được tín hiệu từ BoardWidget"""
        print(f"Controller nhận tín hiệu đánh cờ tại: ({row}, {col})")
        
        # Nếu ô trống thì mới cho phép đánh
        if game_matrix[row][col] == 0:
            # Cập nhật ma trận logic
            game_matrix[row][col] = current_turn[0]
            
            # Đổi lượt chơi
            current_turn[0] = 2 if current_turn[0] == 1 else 1
            
            # GỌI HÀM ĐỒNG BỘ: Đẩy ma trận xuống cho BoardWidget tự xử lý giao diện
            board.sync_board(game_matrix)

    # Controller "Lắng nghe" tín hiệu tổng từ BoardWidget
    board.clicked_signal.connect(on_board_clicked)
    
    # Hiển thị
    board.show()
    app.exec()