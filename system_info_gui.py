# filename = system_info_base.py

from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt
from system_info import SystemInfoFactory
from system_diagnostics import SystemDiagnostics  # Make sure to import SystemDiagnostics

class SystemInfoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Information")
        self.setGeometry(100, 100, 600, 400)
        
        # Set PyOneDark theme (custom style for now)
        self.setStyleSheet("background-color: #282c34; color: #abb2bf;")

        self.layout = QVBoxLayout()
        
        # Button to get system info
        self.info_button = QPushButton("Get System Info")
        self.info_button.setFont(QFont("Arial", 12))
        self.info_button.setStyleSheet("background-color: #61afef; color: white;")
        self.info_button.clicked.connect(self.show_system_info)

        # Button to run diagnostics
        self.diagnostics_button = QPushButton("Run Diagnostics")
        self.diagnostics_button.setFont(QFont("Arial", 12))
        self.diagnostics_button.setStyleSheet("background-color: #61afef; color: white;")
        self.diagnostics_button.clicked.connect(self.run_diagnostics)

        # Text area to display system info
        self.text_area = QTextEdit()
        self.text_area.setFont(QFont("Consolas", 10))
        self.text_area.setStyleSheet("background-color: #21252b; color: #abb2bf;")
        self.text_area.setReadOnly(True)
        
        self.layout.addWidget(self.info_button)
        self.layout.addWidget(self.diagnostics_button)
        self.layout.addWidget(self.text_area)
        self.setLayout(self.layout)

    def show_system_info(self):
        system_info = SystemInfoFactory.get_system_info()
        info = system_info.get_info()
        formatted_info = self.format_info(info)
        self.text_area.setText(formatted_info)

    def run_diagnostics(self):
        diagnostics = SystemDiagnostics()
        diagnostic_results = diagnostics.run_diagnostics()
        formatted_diagnostics = self.format_info(diagnostic_results)
        self.text_area.setText(formatted_diagnostics)

    def format_info(self, info):
        formatted = ""
        for category, details in info.items():
            formatted += f"{category}:\n"
            if isinstance(details, dict):  # Check if details is a dictionary
                for key, value in details.items():
                    formatted += f"  {key}: {value}\n"
            else:
                formatted += f"  {details}\n"  # If it's not a dictionary, just add the string
            formatted += "\n"
        return formatted

if __name__ == "__main__":
    app = QApplication([])
    window = SystemInfoGUI()
    window.show()
    app.exec_()
