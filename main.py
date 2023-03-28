import sys

from back import *
from front import Ui_MainWindow
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg


class GeomWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self._is_vertical_view = True

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.matplotlib_layout.addWidget(self.toolbar)
        self.matplotlib_layout.addWidget(self.canvas)

        self.output.setStyleSheet("background-color: white;")

        d1, d2, d3 = self.d1_spinbox.value(), self.d2_spinbox.value(), self.d3_spinbox.value()
        h1, h2 = self.r1_spinbox.value(), self.r2_spinbox.value()
        t1, t2 = self.t1_spinbox.value(), self.t2_spinbox.value()

        self.model = Geometry(h1, h2, d1, d2, d3, t1, t2)
        self.painter = Painter(self.axes, self.model)

        self.optics_button.clicked.connect(self.draw_optics)
        self.reflections_button.clicked.connect(self.draw_reflections)

    def draw_optics(self) -> None:
        self.painter.draw_optic_2d()

    def draw_reflections(self) -> None:
        self.painter.draw_reflections()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = GeomWindow()
    w.show()

    app.exec()
