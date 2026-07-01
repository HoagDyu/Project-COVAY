<<<<<<< HEAD
# File khởi chạy ứng dụng (Entry point)
=======

import sys
from PyQt6.QtWidgets import QApplication, QWidget
from view.main_window import MainWindow
def main():
    # 1. Create the application instance
    app = QApplication(sys.argv)
    # 2. Create the main window
    window = MainWindow(app=app)
    # 3. Show the window
    window.show()
    # 4. Run the application's event loop safely
    app.exec()
if __name__ == '__main__':
    main()
>>>>>>> master
