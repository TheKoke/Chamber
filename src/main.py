import sys

from PyQt5.QtWidgets import QApplication
from frontend.startwindow import StartWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = StartWindow()
    w.show()
    app.exec()