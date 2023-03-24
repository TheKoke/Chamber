import sys

from back import *
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg


class GeomWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setGeometry(0, 0, 1300, 900)

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3)))
        self.axes = self.canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = GeomWindow()
    w.show()

    app.exec()
