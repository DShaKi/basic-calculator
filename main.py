from PyQt5.QtWidgets import QApplication
from ui.calculator_ui import CalculatorUI
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())