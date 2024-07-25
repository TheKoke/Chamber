from backend.geometry import Geometry
from backend.spot import SpotModel

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg


class SpotWindow(QWidget):
    def __init__(self, geometry: Geometry) -> None:
        super().__init__()
        self.setWindowTitle('Looking at spot - Chamber')
        self.setWindowIcon(QIcon('./icon.ico'))

        self.view = FigureCanvasQTAgg(Figure(figsize=(9, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view)

        self.spot = SpotModel(self.axes, geometry)

        self.view.figure.tight_layout()

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.view)
        self.setLayout(vlayout)

        self.start()

    def start(self) -> None:
        self.spot.draw()
        self.view.draw()


if __name__ == '__main__':
    pass
