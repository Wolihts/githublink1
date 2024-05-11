from PyQt6.QtWidgets import *
from view import *
import sys

def main():
    app = QApplication(sys.argv)
    v = View()
    v.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

# https://realpython.com/python-pyqt-gui-calculator/ used as a guide for my code
# https://www.youtube.com/watch?v=2XdhmcyAnH0 used as a starting point