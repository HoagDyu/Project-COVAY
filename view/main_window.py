# Cửa sổ chính, ghép các widget lại với nhau
import sys
from PyQt6.QtWidgets import QApplication, QWidget
def main():
    # 1. Create the application instance
    app = QApplication(sys.argv)
    # 2. Create the main window
    window = QWidget()
    window.setWindowTitle("My First PyQt6 App")
    
    # Set the window dimensions (x, y, width, height)
    window.setGeometry(100, 100, 400, 300) 
    # 3. Show the window
    window.show()
    # 4. Run the application's event loop safely
    sys.exit(app.exec())
if __name__ == '__main__':
    main()
