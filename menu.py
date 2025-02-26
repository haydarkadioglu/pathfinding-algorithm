import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from grid import GridGUI

class MenuWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app  # Store QApplication reference
        self.setWindowTitle("Pathfinding Visualizer")
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
        self.confirm_button = QPushButton("Start Visualization")
        self.confirm_button.clicked.connect(self.create_visualization)
        layout.addWidget(self.confirm_button)
        
        # Add error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

    def create_visualization(self):
        try:
            size = int(self.size_input.text())
            if 8 <= size <= 32:
                self.hide()  # Hide instead of close
                self.app.processEvents()  # Process any pending events
                
                # Create and run visualization
                gui = GridGUI(800, size)
                gui.run()
                
                # After visualization closes, close the menu
                self.close()
                self.app.quit()
            else:
                self.error_label.setText("Please enter a number between 8 and 32")
        except ValueError:
            self.error_label.setText("Please enter a valid number")

