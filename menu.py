import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt
from grid import GridGUI
from stops_mode import StopsMode

class MenuWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app  # Store QApplication reference
        self.setWindowTitle("Pathfinding Visualizer")
        self.setFixedSize(300, 250)  # Made window slightly taller
        
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
        
        # Add mode selection
        self.mode_group = QButtonGroup()
        normal_mode = QRadioButton("Normal Mode")
        stops_mode = QRadioButton("Stops Mode")
        normal_mode.setChecked(True)
        self.mode_group.addButton(normal_mode, 0)
        self.mode_group.addButton(stops_mode, 1)
        layout.addWidget(normal_mode)
        layout.addWidget(stops_mode)
        
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
                
                # Create visualization based on selected mode
                if self.mode_group.checkedId() == 0:
                    gui = GridGUI(800, size)
                else:
                    gui = StopsMode(800, size)
                gui.run()
                
                # After visualization closes, close the menu
                self.close()
                self.app.quit()
            else:
                self.error_label.setText("Please enter a number between 8 and 32")
        except ValueError:
            self.error_label.setText("Please enter a valid number")

