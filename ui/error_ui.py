from PyQt5.QtWidgets import QMessageBox, QWidget

class Error(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error!")

    def show_error_message(self, exception):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")

        if isinstance(exception, ZeroDivisionError):
            msg.setText("Math error: Division by zero is not allowed.")
        elif isinstance(exception, ValueError):
            msg.setText("Value error: Invalid input provided.")
        else:
            msg.setText("An unexpected error occurred.")
        
        msg.setInformativeText(str(exception))
        msg.exec_()