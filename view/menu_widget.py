from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
)
from core.constant import StoneColor

import sys
import os
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QPushButton, QComboBox, QLabel, QFrame
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6 import uic


class MenuWidget(QWidget):
    btn_pvp: QPushButton
    btn_pve: QPushButton
    btn_exit: QPushButton
    bot_color_combo: QComboBox
    size_combo: QComboBox
    time_combo: QComboBox
    lbl_title: QLabel
    frame: QFrame

    pvp_start_signal = pyqtSignal()
    pve_start_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # Đường dẫn tới file menu.ui cùng thư mục
        ui_path = os.path.join(os.path.dirname(__file__), 'menu2.ui')
        
        # Nạp giao diện từ file .ui vào widget này
        self.ui = uic.loadUi(ui_path, self)
        
        self.setWindowTitle("Menu Cờ Vây")

        # ---- Load ảnh nền ----
        bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")
        self.background_pixmap = QPixmap(bg_path)
        
        # Kết nối sự kiện click của các nút bấm (tên nút dựa theo objectName trong file .ui)
        self.btn_pvp.clicked.connect(self.start_player_vs_player)
        self.btn_pve.clicked.connect(self.start_player_vs_ai)
        self.btn_exit.clicked.connect(self.close)

        self.bot_color_combo.addItem("Choose Bot Color", StoneColor.EMPTY)
        self.bot_color_combo.addItem("Bot plays White", StoneColor.WHITE)
        self.bot_color_combo.addItem("Bot plays Black", StoneColor.BLACK)

        self.size_combo.addItem("19x19",19,)
        self.size_combo.addItem("13x13",13)
        self.size_combo.addItem("9x9",9)

        self.time_combo.addItem("5m",5)
        self.time_combo.addItem("15m",15)
        self.time_combo.addItem("30m",30)
        
        self.set_up_color()

    def paintEvent(self, event):
        # Vẽ ảnh nền phủ toàn bộ widget, tự stretch theo kích thước cửa sổ
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)
        super().paintEvent(event)

    def set_up_color(self):

        # Đảm bảo frame vẽ được background theo QSS
        self.frame.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.horizontalLayout_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QFrame#frame {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 15px;
            }
            QPushButton {
                background-color: rgba(168, 126, 98, 255);
                color: #3a2317;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 25px;
                min-height: 60px;
                max-height: 60px;
                min-width: 150px;
                max-width: 150px;
            }
            QPushButton:hover { background-color: #b07154; }
            QPushButton:pressed { background-color: #3a2317; }
            QComboBox {
                background-color: rgba(168, 126, 98, 255);
                color: #3a2317;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 25px;
                min-height: 60px;
                max-height: 60px;
                min-width: 550px;
                max-width: 550px;
                
            }
            QComboBox QAbstractItemView {
                background-color: rgba(168, 126, 98, 150);
                color: #3a2317;
                selection-background-color: rgba(168, 126, 98, 150);  
                selection-color: #311f13;                
                outline: none;                          
                border: 1px solid #555;
            }
            QLabel{
                color: #f4decb;
                background: transparent;
                margin: 10px;
                font-weight: bold;
                font-size: 70px;
            }
        """)

    def start_player_vs_player(self):
        self.pvp_start_signal.emit()

    def start_player_vs_ai(self):
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