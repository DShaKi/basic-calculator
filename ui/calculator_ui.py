from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from ui.error_ui import Error
import math
import re

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basic Calculator")
        self.setGeometry(100, 100, 300, 400)
        
        self.create_ui()
        
    def create_ui(self):
        main_layout = QVBoxLayout()
        
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(40)
        self.display.setStyleSheet("font-size: 20px; padding: 5px;")
        main_layout.addWidget(self.display)
        
        buttons_layout = QGridLayout()
        
        buttons = [
            "C/CE", '+/-', '√', '%',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        row, col = 0, 0
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedSize(60, 60)
            button.setStyleSheet("font-size: 18px;")
            button.clicked.connect(lambda checked, bt=button_text: self.button_clicked(bt))
            buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def button_clicked(self, button_text):
        text = self.display.text()
        if button_text == "=":
            if '√' in text:
                text = text.replace("√", "sqrt(")
                text = re.sub(r"sqrt\((\d+)", r"sqrt(\1)", text)
            try:
                result = str(eval(text, {"__builtins__": None}, {'sqrt': math.sqrt}))
                self.display.setText(result)
            except Exception as e:
                error = Error()
                error.show_error_message(e)
        elif button_text == '+/-':
            match = re.search(r"([-]?\d*\.?\d+)$", text)
            print(match)
            if match:
                number = match.group(1)
                start, end = match.span(1)
                if number.startswith("-"):
                    new_number = number[1:]
                else:
                    new_number = "-" + number
                self.display.setText(text[:int(start)] + new_number)
        elif button_text == 'C/CE':
            self.display.setText('')
        else:
            self.display.setText(text + button_text)