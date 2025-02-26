import sys
from PyQt5.QtWidgets import QApplication
from menu import MenuWindow

def main():
    app = QApplication(sys.argv)
    window = MenuWindow(app)  # Pass app reference to window
    window.show()
    sys.exit(app.exec_())  # Use sys.exit to ensure clean shutdown

if __name__ == "__main__":
    main()