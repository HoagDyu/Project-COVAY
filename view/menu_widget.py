from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
)
from core.constant import StoneColor

import sys
import os
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6 import uic

class MenuWidget(QWidget):
    pvp_start_signal = pyqtSignal()
    pve_start_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # Đường dẫn tới file menu.ui cùng thư mục
        ui_path = os.path.join(os.path.dirname(__file__), 'menu.ui')
        
        # Nạp giao diện từ file .ui vào widget này
        self.ui = uic.loadUi(ui_path, self)
        
        self.setWindowTitle("Menu Cờ Vây")
        
        # Kết nối sự kiện click của các nút bấm (tên nút dựa theo objectName trong file .ui)
        self.btn_pvp.clicked.connect(self.start_player_vs_player)
        self.btn_pve.clicked.connect(self.start_player_vs_ai)
        self.btn_exit.clicked.connect(self.close)

        self.ui.bot_color_combo.addItem("Choose Bot Color", StoneColor.EMPTY)
        self.ui.bot_color_combo.addItem("Bot plays White", StoneColor.WHITE)
        self.ui.bot_color_combo.addItem("Bot plays Black", StoneColor.BLACK)

        self.ui.size_combo.addItem("19x19",19,)
        self.ui.size_combo.addItem("13x13",13)
        self.ui.size_combo.addItem("9x9",9)

        self.ui.time_combo.addItem("5m",5)
        self.ui.time_combo.addItem("15m",15)
        self.ui.time_combo.addItem("30m",30)
        

    def start_player_vs_player(self):
        QMessageBox.information(self, "Thông báo", "Bắt đầu chế độ: Người chơi vs Người chơi!")
        self.pvp_start_signal.emit()

    def start_player_vs_ai(self):
        QMessageBox.information(self, "Thông báo", "Bắt đầu chế độ: Người chơi vs Máy!")
        self.pve_start_signal.emit()
    
    def get_size(self) -> int:
        return int(self.ui.size_combo.currentData())

    def get_bot(self) -> tuple[bool, StoneColor]:
        return True, self.ui.bot_color_combo.currentData()
    
    def get_time(self) -> int:
        return self.ui.time_combo.currentData()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Khởi tạo và hiển thị MenuWidget đầu tiên khi chạy app
    menu_app = MenuWidget()
    menu_app.show()
    
    sys.exit(app.exec())