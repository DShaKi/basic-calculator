from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDockWidget, QListWidget
from ui.components import Button, IconButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSettings
from logic.calculator_logic import change_eval_symbols, calculate
from ui.error_ui import Error
import re

def load_stylesheet(path):
    with open(path, 'r') as f:
        return f.read()

light_stylesheet = load_stylesheet('ui/styles/light.qss')
dark_stylesheet = load_stylesheet('ui/styles/dark.qss')

class CalculatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mode = None

        self.history = []

        self.base_width = 350
        self.base_height = 550
        self.expanded_width = 550

        self.setWindowTitle("Basic Calculator")
        self.icon = QIcon("assets/icons/calculator.ico")
        self.setMinimumSize(self.base_width, self.base_height)
        self.setMaximumSize(self.expanded_width, self.base_height)
        self.setWindowIcon(self.icon)
        self.setGeometry(100, 100, 300, 400)
        
        self.settings = QSettings("MagicCo", "CalculatorApp")
        
        self.create_ui()
        self.load_settings()

    def create_ui(self):
        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.base_width, self.base_height)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.display = QLineEdit()
        self.display.setFixedHeight(80)
        self.display.setFont(QFont("Helvetica", 24))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            background-color: #222;
            color: white;
            border-radius: 10px;
            padding-right: 15px;
        """)
        self.display.returnPressed.connect(lambda t=self.display.text(): self.on_enter_pressed(t))
        self.main_layout.addWidget(self.display)

        self.top_bar = QHBoxLayout()
        self.main_layout.addLayout(self.top_bar)

        self.toggle_dark_mode_btn = Button("Toggle Dark Mode")
        self.toggle_dark_mode_btn.setFixedHeight(50)
        self.toggle_dark_mode_btn.setFont(QFont("Helvetica", 12))
        self.toggle_dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        self.top_bar.addWidget(self.toggle_dark_mode_btn)

        history_icon_paths = {"light_normal": "assets/icons/light_normal_history.ico", "light_hover": "assets/icons/light_hover_history.ico", "dark_normal": "assets/icons/dark_normal_history.ico", "dark_hover": "assets/icons/dark_hover_history.ico"}
        self.history_btn = IconButton(history_icon_paths, self.mode)
        self.history_btn.setFixedSize(50, 50)
        self.history_btn.clicked.connect(self.toggle_history_panel)
        self.top_bar.addWidget(self.history_btn)

        self.history_panel = QDockWidget("", self)
        self.history_panel.setAllowedAreas(Qt.RightDockWidgetArea)
        self.history_panel.setFixedSize(200, self.base_height)
        self.history_list = QListWidget()
        self.history_panel.setWidget(self.history_list)
        self.history_panel.setVisible(False)
        self.history_panel.setFeatures((QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable) & ~QDockWidget.DockWidgetClosable)
        self.history_panel.setTitleBarWidget(QWidget())
        self.addDockWidget(Qt.RightDockWidgetArea, self.history_panel)

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
            btn = Button(btn_text)
            btn.setFixedSize(70, 70)
            btn.setFont(QFont("Helvetica", 18))
            btn.setStyleSheet(self.button_style(btn_text))
            btn.clicked.connect(lambda checked, b=btn_text: self.on_button_clicked(b))
            buttons_layout.addWidget(btn, row, col)
            self.buttons[btn_text] = btn
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.main_layout.addLayout(buttons_layout)

        self.central_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.central_widget)


    def button_style(self, btn_text):
        if btn_text in ['C', '+/-', '√', '%']:
            return "background-color: #555; color: white; border-radius: 15px;"
        elif btn_text in ['÷', '×', '-', '+', '=']:
            return "background-color: #ff9500; color: white; border-radius: 15px;"
        else:
            return "background-color: #333; color: white; border-radius: 15px;"

    def on_button_clicked(self, button_text):
        text = self.display.text()
        if button_text == "=":
            text = change_eval_symbols(text)
            try:
                result = calculate(text)
                self.display.setText(result)
                self.add_to_history(text, result)
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

    def on_enter_pressed(self, text):
        self.display.setText(calculate(text))

    def toggle_dark_mode(self):
        if self.styleSheet() == dark_stylesheet:
            self.setStyleSheet(light_stylesheet)
            self.history_btn.toggle_mode("light")
            self.settings.setValue("dark_mode", False)
        else:
            self.setStyleSheet(dark_stylesheet)
            self.history_btn.toggle_mode("dark")
            self.settings.setValue("dark_mode", True)

    def add_to_history(self, operation, result):
        history_text = f"{operation}\n{result}"
        self.history.append((operation, result))
        self.history_list.addItem(history_text)

    def toggle_history_panel(self):
        if self.history_panel.isVisible():
            self.history_panel.hide()
            self.setFixedSize(self.base_width, self.base_height)
        else:
            self.history_panel.show()
            self.setMinimumSize(self.base_width, self.base_height)
            self.setMaximumSize(self.expanded_width, self.base_height)
            self.resize(self.expanded_width, self.base_height)
            self.setFixedSize(self.expanded_width, self.base_height)

    def load_settings(self):
        self.mode = self.settings.value("dark_mode", False, type=bool)
        if self.mode:
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet(light_stylesheet)