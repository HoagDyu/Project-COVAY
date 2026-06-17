from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
import os

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Go Game")
        
 