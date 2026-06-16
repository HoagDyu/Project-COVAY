from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
import os

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.UwU_clicked = 0
        self.UwU_text = ""
        
        ui_path = os.path.join("test_main_window.ui")

        uic.loadUi(ui_path, self)

        self.lcdNumber.display(self.UwU_clicked)
        self.UwU_button.clicked.connect(self.handle_click)
        self.clear_button.clicked.connect(self.handle_clear_button_click)
        self.label.setText(self.UwU_text)
        
    def handle_click(self):
        print("UwU")
        self.UwU_clicked +=1
        self.UwU_text = "UwU"
        self.lcdNumber.display(self.UwU_clicked)
        self.label.setText(self.UwU_text)
        
        
    def handle_clear_button_click(self):
        print("Quieeeee")
        self.UwU_clicked = 0
        self.UwU_text = "Clear"
        self.lcdNumber.display(self.UwU_clicked)
        self.label.setText(self.UwU_text)
        
 