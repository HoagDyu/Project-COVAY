
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from view.main_window import MainWindow
from controller.game_manager import GameController
def main():
    # 1. Create the application instance
    app = QApplication(sys.argv)
    # 2. Create the main window
    window = MainWindow(app=app)
    controller = GameController(window)
    window.controller = controller  # giữ reference, tránh bị garbage collect
    # 3. Show the window
    window.show()
    # 4. Run the application's event loop safely
    app.exec()
if __name__ == '__main__':
    main()
