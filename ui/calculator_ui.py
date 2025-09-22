from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from logic.calculator_logic import change_symbols 
from ui.error_ui import Error
import math
import re

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basic Calculator")
        self.icon = QIcon("assets/img/calculator_icon.png")
        self.setWindowIcon(self.icon)
        self.setGeometry(100, 100, 300, 400)
        self.setFixedSize(350, 500)
        
        self.create_ui()
        
    def create_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setFont(QFont("Helvetica", 24))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            background-color: #222;
            color: white;
            border-radius: 10px;
            padding-right: 15px;
        """)
        main_layout.addWidget(self.display)

        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(8)

        buttons = [
            'C', '+/-', '√', '%',
            '7', '8', '9', '÷',
            '4', '5', '6', '×',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        self.buttons = {}
        row, col = 0, 0
        for btn_text in buttons:
            btn = QPushButton(btn_text)
            btn.setFixedSize(70, 70)
            btn.setFont(QFont("Helvetica", 18))
            btn.setStyleSheet(self.button_style(btn_text))
            btn.clicked.connect(lambda checked, b=btn_text: self.button_clicked(b))
            buttons_layout.addWidget(btn, row, col)
            self.buttons[btn_text] = btn
            col += 1
            if col > 3:
                col = 0
                row += 1

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def button_style(self, btn_text):
        if btn_text in ['C', '+/-', '√', '%']:
            return "background-color: #555; color: white; border-radius: 15px;"
        elif btn_text in ['÷', '×', '-', '+', '=']:
            return "background-color: #ff9500; color: white; border-radius: 15px;"
        else:
            return "background-color: #333; color: white; border-radius: 15px;"

    def button_clicked(self, button_text):
        text = self.display.text()
        if button_text == "=":
            text = change_symbols(text)
            try:
                result = eval(text, {"__builtins__": None}, {'sqrt': math.sqrt})
                result = round(result, 10)
                result = str(result)
                self.display.setText(result)
            except Exception as e:
                error = Error()
                error.show_error_message(e)
        elif button_text == '+/-':
            match = re.search(r"([-]?\d*\.?\d+)$", text)
            if match:
                number = match.group(1)
                start, end = match.span(1)
                if number.startswith("-"):
                    new_number = number[1:]
                else:
                    new_number = "-" + number
                self.display.setText(text[:int(start)] + new_number)
        elif button_text == 'C':
            self.display.setText('')
        else:
            self.display.setText(text + button_text)