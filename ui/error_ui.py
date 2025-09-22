from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon

class Error(QWidget):
    def show_error_message(self, e):
        msg = QMessageBox(self)
        icon = QIcon("assets/img/error_icon.png")
        msg.setWindowIcon(icon)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error!")
        font = QFont("Helvetica", 10)
        msg.setFont(font)
        if isinstance(e, ZeroDivisionError):
            msg.setText("Math error: Division by zero is not allowed.")
        elif isinstance(e, ValueError):
            msg.setText("Value error: Invalid input provided.")
        else:
            msg.setText("An unexpected error occurred.")
        msg.setInformativeText(str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()