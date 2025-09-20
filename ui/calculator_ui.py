from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from logic import calculator_logic

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
        nums = { '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.' }
        funcs = { '+', '*', '-', '/' }
        if button_text == "=":
            result = str(eval(self.display.text()))
            self.display.setText(result)
        else:
            text = self.display.text()
            self.display.setText(text + button_text)