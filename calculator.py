import os.path
import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

# Load the DLL
dll = os.path.join(os.path.dirname(__file__), "CmakeCalculator.dll")
calculator = ctypes.CDLL(dll)

# Define the argument and return types for the float functions
calculator.add.argtypes = [ctypes.c_float, ctypes.c_float]
calculator.add.restype = ctypes.c_float

calculator.subtract.argtypes = [ctypes.c_float, ctypes.c_float]
calculator.subtract.restype = ctypes.c_float

calculator.multiply.argtypes = [ctypes.c_float, ctypes.c_float]
calculator.multiply.restype = ctypes.c_float

calculator.divide.argtypes = [ctypes.c_float, ctypes.c_float]
calculator.divide.restype = ctypes.c_float

calculator.sine.argtypes = [ctypes.c_float]
calculator.sine.restype = ctypes.c_float

calculator.cosine.argtypes = [ctypes.c_float]
calculator.cosine.restype = ctypes.c_float

calculator.tangent.argtypes = [ctypes.c_float]
calculator.tangent.restype = ctypes.c_float

calculator.logarithm.argtypes = [ctypes.c_float]
calculator.logarithm.restype = ctypes.c_float

calculator.exponentiate.argtypes = [ctypes.c_float, ctypes.c_float]
calculator.exponentiate.restype = ctypes.c_float

calculator.square_root.argtypes = [ctypes.c_float]
calculator.square_root.restype = ctypes.c_float

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the layout
        vbox = QVBoxLayout()

        # Display
        self.display = QLineEdit(self)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Arial', 20))
        vbox.addWidget(self.display)

        # Button grid
        grid = QGridLayout()

        buttons = [
            # Row 1
            ('SHIFT', 0, 0), ('ALPHA', 0, 1), ('MODE', 0, 2), ('DEL', 0, 3),
            # Row 2
            ('(', 1, 0), (')', 1, 1), ('%', 1, 2), ('AC', 1, 3),
            # Row 3
            ('sin', 2, 0), ('cos', 2, 1), ('tan', 2, 2), ('log', 2, 3),
            # Row 4
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
            # Row 5
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
            # Row 6
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
            # Row 7
            ('0', 6, 0), ('.', 6, 1), ('EXP', 6, 2), ('+', 6, 3),
            # Row 8
            ('Ans', 7, 0), ('ENG', 7, 1), ('(', 7, 2), ('=', 7, 3),
        ]

        button_colors = {
            'SHIFT': '#FFD700', 'ALPHA': '#FF4500', 'MODE': '#4682B4', 'DEL': '#FF6347',
            'AC': '#FF6347', '=': '#32CD32', 'EXP': '#FFD700', 'Ans': '#87CEFA',
            'sin': '#4682B4', 'cos': '#4682B4', 'tan': '#4682B4', 'log': '#4682B4',
            '0': '#D3D3D3', '1': '#D3D3D3', '2': '#D3D3D3', '3': '#D3D3D3',
            '4': '#D3D3D3', '5': '#D3D3D3', '6': '#D3D3D3', '7': '#D3D3D3',
            '8': '#D3D3D3', '9': '#D3D3D3', '.': '#D3D3D3', '+': '#D3D3D3',
            '-': '#D3D3D3', '*': '#D3D3D3', '/': '#D3D3D3'
        }

        for btn_text, x, y in buttons:
            btn = QPushButton(btn_text, self)
            btn.setFont(QFont('Arial', 14))
            btn.setFixedSize(70, 50)
            btn.setStyleSheet(f"background-color: {button_colors.get(btn_text, '#D3D3D3')};")
            grid.addWidget(btn, x, y)
            btn.clicked.connect(self.on_click)

        vbox.addLayout(grid)
        self.setLayout(vbox)

        self.setWindowTitle('Scientific Calculator')
        self.setGeometry(100, 100, 400, 500)

    def on_click(self):
        sender = self.sender()
        text = sender.text()

        if text == 'AC':
            self.display.clear()
        elif text == 'DEL':
            current_text = self.display.text()
            self.display.setText(current_text[:-1])
        elif text == '=':
            self.calculate()
        elif text in ['sin', 'cos', 'tan', 'log', 'sqrt']:
            self.calculate_scientific(text)
        else:
            self.display.setText(self.display.text() + text)

    def calculate(self):
        try:
            expression = self.display.text()
            result = eval(expression, {"__builtins__": None}, {
                "add": calculator.add,
                "subtract": calculator.subtract,
                "multiply": calculator.multiply,
                "divide": calculator.divide,
                "exponentiate": calculator.exponentiate
            })
            self.display.setText(str(result))
        except Exception as e:
            self.display.setText('Error')

    def calculate_scientific(self, operation):
        try:
            value = float(self.display.text())
            result = 0.0
            if operation == 'sin':
                result = calculator.sine(value)
            elif operation == 'cos':
                result = calculator.cosine(value)
            elif operation == 'tan':
                result = calculator.tangent(value)
            elif operation == 'log':
                result = calculator.logarithm(value)
            elif operation == 'sqrt':
                result = calculator.square_root(value)

            self.display.setText(str(result))
        except Exception as e:
            self.display.setText('Error')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculatorApp()
    ex.show()
    sys.exit(app.exec_())
