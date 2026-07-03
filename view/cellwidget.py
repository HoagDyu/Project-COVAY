import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt

class CellWidget(QPushButton):
    # Tạo một custom signal để truyền tọa độ (row, col) ra ngoài khi được click
    clicked_pos = pyqtSignal(int, int)

    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        
        # 1. Lưu giữ tọa độ
        self.row = row
        self.col = col
        
        # Trạng thái ô cờ: 0 = Rỗng, 1 = Đen, 2 = Trắng
        self.state = 0 
        
        # Thiết lập kích thước cố định cho mỗi ô cờ (ví dụ: 40x40 pixel)
        self.setFixedSize(40, 40)
        
        # Bỏ viền mặc định của button để hiển thị đẹp hơn trên lưới
        self.setFlat(True) 
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Áp dụng giao diện ban đầu
        self.update_style()
        
        # 4. Bắt sự kiện click chuột
        self.clicked.connect(self.on_click)

    # 2. Thay đổi giao diện dựa trên trạng thái
    def set_state(self, state):
        """Cập nhật trạng thái của ô và đổi màu tương ứng"""
        self.state = state
        self.update_style()

    def update_style(self):
        """Sử dụng QSS (Qt Style Sheets) để vẽ quân cờ và tạo hiệu ứng hover"""
        if self.state == 1:
            # Quân Đen
            self.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    border-radius: 18px; /* Bo tròn để tạo hình tròn */
                    margin: 2px;         /* Tạo khoảng cách để không bị sát viền ô */
                }
            """)
        elif self.state == 2:
            # Quân Trắng
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border-radius: 18px;
                    margin: 2px;
                    border: 1px solid #333; /* Viền nhẹ để phân biệt với nền sáng nếu có */
                }
            """)
        else:
            # 3. Rỗng & Tạo hiệu ứng Hover
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent; /* Trong suốt để lộ đường kẻ caro của bàn cờ ở dưới */
                    border: none;
                }
                QPushButton:hover {
                    /* Khi di chuột qua ô rỗng, hiển thị một bóng mờ (gợi ý đặt cờ) */
                    background-color: rgba(0, 0, 0, 0.2); 
                    border-radius: 18px;
                    margin: 2px;
                }
            """)

    def on_click(self):
        """Hàm xử lý khi nút bị click"""
        # Phát tín hiệu mang theo tọa độ của chính nó
        self.clicked_pos.emit(self.row, self.col)

# =========================================
# CODE TEST THỬ NGHIỆM (Chạy file để xem kết quả)
# =========================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Tạo một cửa sổ giả lập một góc bàn cờ
    window = QWidget()
    window.setWindowTitle("Test CellWidget - Cờ Vây")
    window.setStyleSheet("background-color: #DCB35C;") # Màu nền gỗ bàn cờ vây
    layout = QGridLayout(window)
    layout.setSpacing(0) # Bàn cờ vây các ô sát nhau

    def handle_click(row, col):
        print(f"Bạn vừa click vào ô tọa độ: Hàng {row}, Cột {col}")
        # Giả lập logic: click vào ô rỗng thì đánh cờ đen
        cell = cells[(row, col)]
        if cell.state == 0:
            cell.set_state(1)

    cells = {}
    # Tạo lưới 5x5 để test
    for r in range(5):
        for c in range(5):
            cell = CellWidget(r, c)
            cell.clicked_pos.connect(handle_click)
            layout.addWidget(cell, r, c)
            cells[(r, c)] = cell

    # Thử set sẵn 1 quân trắng, 1 quân đen
    cells[(2, 2)].set_state(1) # Đen
    cells[(2, 3)].set_state(2) # Trắng

    window.show()
    