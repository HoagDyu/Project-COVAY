from PyQt6.QtWidgets import QWidget
from PyQt6 import uic 
import os


class PanelWidget(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join("panel.ui")
        uic.loadUI(ui_path,self)

        # Kết nối các nút
        self.ui.pushButton.clicked.connect(self.new_game)
        self.ui.pushButton_5.clicked.connect(self.undo)
        self.ui.pushButton_3.clicked.connect(self.resign)
        self.ui.pushButton_6.clicked.connect(self.save_game)
        self.ui.pushButton_4.clicked.connect(self.load_game)
        self.ui.pushButton_2.clicked.connect(self.exit_game)

    def new_game(self):
        print("Bắt đầu ván mới")

    def undo(self):
        print("Hoàn tác nước đi")

    def resign(self):
        print("Người chơi đầu hàng")

    def save_game(self):
        print("Lưu ván cờ")

    def load_game(self):
        print("Mở ván cờ")

    def exit_game(self):
        self.close()
