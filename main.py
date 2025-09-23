from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.calculator_ui import CalculatorUI
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icons/calculator.ico"))
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())