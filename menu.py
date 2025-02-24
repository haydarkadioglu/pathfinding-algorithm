from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
import sys
from grid import Grid

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grid Size Selection")
        self.setFixedSize(300, 200)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add title label
        title = QLabel("Enter Grid Size (8-32):")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Add input field
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Enter a number (e.g., 16)")
        self.size_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.size_input)
        
        # Add confirm button
        self.confirm_button = QPushButton("Create Grid")
        self.confirm_button.clicked.connect(self.create_grid)
        layout.addWidget(self.confirm_button)
        
        # Add error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

    def create_grid(self):
        try:
            size = int(self.size_input.text())
            if 8 <= size <= 32:
                self.close()
                grid = Grid(800, size)
                grid.run()
            else:
                self.error_label.setText("Please enter a number between 8 and 32")
        except ValueError:
            self.error_label.setText("Please enter a valid number")

def main():
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()