import sys
import os
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6 import uic

class MenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Đường dẫn tới file menu.ui cùng thư mục
        ui_path = os.path.join(os.path.dirname(__file__), 'menu.ui')
        
        # Nạp giao diện từ file .ui vào widget này
        uic.loadUi(ui_path, self)
        
        self.setWindowTitle("Menu Cờ Vây")
        
        # Kết nối sự kiện click của các nút bấm (tên nút dựa theo objectName trong file .ui)
        self.btn_pvp.clicked.connect(self.start_player_vs_player)
        self.btn_pve.clicked.connect(self.start_player_vs_ai)
        self.btn_exit.clicked.connect(self.close)

    def start_player_vs_player(self):
        # Nơi xử lý khi người dùng chọn Người vs Người
        QMessageBox.information(self, "Thông báo", "Bắt đầu chế độ: Người chơi vs Người chơi!")
        # Bạn có thể import BoardWidget từ board_widget.py ở đây để hiển thị bàn cờ
        # self.board = BoardWidget()
        # self.board.show()
        # self.close()

    def start_player_vs_ai(self):
        # Nơi xử lý khi người dùng chọn Người vs Máy
        QMessageBox.information(self, "Thông báo", "Bắt đầu chế độ: Người chơi vs Máy!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Khởi tạo và hiển thị MenuWidget đầu tiên khi chạy app
    menu_app = MenuWidget()
    menu_app.show()
    
    sys.exit(app.exec())