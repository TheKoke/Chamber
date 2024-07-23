import sys

from PyQt5.QtWidgets import QApplication
from frontend.geomwindow import GeomWindow
from backend.start import starting_position


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GeomWindow(starting_position())
    w.show()
    app.exec()
