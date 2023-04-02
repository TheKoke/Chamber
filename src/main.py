import sys

from back import *
from front import Ui_MainWindow
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg


class SpotWindow(QWidget):
    def __init__(self, r1: float, r2: float, shift_1: float, shift_2: float) -> None:
        super().__init__()

        self.r1 = r1
        self.r2 = r2
        self.shift_1 = shift_1
        self.shift_2 = shift_2

        self.view = FigureCanvasQTAgg(Figure(figsize=(9, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view)

        self.view.figure.tight_layout()

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.view)
        self.setLayout(vlayout)

        self.start()

    def start(self) -> None:
        draw_ellipse(self.axes, self.r1, self.r2, self.shift_1, self.shift_2)

        self.axes.set_ylim(-7, 7)
        self.axes.set_xlim((-7, 7))
        self.axes.set_aspect('equal')


class GeomWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self._is_vertical_view = True

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.canvas.figure.tight_layout()

        self.matplotlib_layout.addWidget(self.toolbar)
        self.matplotlib_layout.addWidget(self.canvas)

        self.output.setStyleSheet("background-color: white;")

        d1, d2, d3 = self.d1_spinbox.value(), self.d2_spinbox.value(), self.d3_spinbox.value()
        h1, h2 = self.r1_spinbox.value(), self.r2_spinbox.value()
        t1, t2 = self.t1_spinbox.value(), self.t2_spinbox.value()

        self.model = Geometry(h1, h2, d1, d2, d3, t1, t2, 'v' if self._is_vertical_view else 'h')
        self.painter = Painter(self.axes, self.model)

        # general properties
        self.d1_spinbox.valueChanged.connect(self.prop_change)
        self.d2_spinbox.valueChanged.connect(self.prop_change)
        self.d3_spinbox.valueChanged.connect(self.prop_change)
        self.r1_spinbox.valueChanged.connect(self.prop_change)
        self.r2_spinbox.valueChanged.connect(self.prop_change)
        self.t1_spinbox.valueChanged.connect(self.prop_change)
        self.t2_spinbox.valueChanged.connect(self.prop_change)

        # tilting properties
        self.up_spinbox_1.valueChanged.connect(self.tilt_change)
        self.down_spinbox_1.valueChanged.connect(self.tilt_change)
        self.right_spinbox_1.valueChanged.connect(self.tilt_change)
        self.left_spinbox_1.valueChanged.connect(self.tilt_change)
        self.up_spinbox_2.valueChanged.connect(self.tilt_change)
        self.down_spinbox_2.valueChanged.connect(self.tilt_change)
        self.right_spinbox_2.valueChanged.connect(self.tilt_change)
        self.left_spinbox_2.valueChanged.connect(self.tilt_change)

        # general buttons
        self.optics_button.clicked.connect(self.draw_optics)
        self.reflections_button.clicked.connect(self.draw_reflections)
        self.view_button.clicked.connect(self.change_view)
        self.spot_button.clicked.connect(self.look_at_spot)

    def __new_model(self) -> None:
        d1, d2, d3 = self.d1_spinbox.value(), self.d2_spinbox.value(), self.d3_spinbox.value()
        h1, h2 = self.r1_spinbox.value(), self.r2_spinbox.value()
        t1, t2 = self.t1_spinbox.value(), self.t2_spinbox.value()

        self.model = Geometry(h1, h2, d1, d2, d3, t1, t2, 'v' if self._is_vertical_view else 'h')
        self.painter = Painter(self.axes, self.model)

    def look_at_spot(self) -> None:
        u1, u2 = self.up_spinbox_1.value(), self.up_spinbox_2.value()
        d1, d2 = self.down_spinbox_1.value(), self.down_spinbox_2.value()
        r1, r2 = self.right_spinbox_1.value(), self.right_spinbox_2.value()
        l1, l2 = self.left_spinbox_1.value(), self.left_spinbox_2.value()

        x_shift = (r2 - l2) - (r1 - l1)
        y_shift = (u2 - d2) - (u1 - d1)

        self.window = SpotWindow(self.r1_spinbox.value(), self.r2_spinbox.value(), x_shift, y_shift)
        self.window.show()

    def prop_change(self) -> None:
        self.clear_output()

        self.axes.clear()
        self.canvas.draw()

        self.__new_model()
        self.do_shifts()

    def tilt_change(self) -> None:
        self.clear_output()

        self.axes.clear()
        self.canvas.draw()

        self.do_shifts()
        
    def do_shifts(self) -> None:
        if self._is_vertical_view:
            ups = self.up_spinbox_1.value(), self.up_spinbox_2.value()
            downs = self.down_spinbox_1.value(), self.down_spinbox_2.value()

            self.__new_model()
            
            for i in range(len(ups)):
                self.model.shift_dots(i, 'up', ups[i])
                self.model.shift_dots(i, 'down', downs[i])
        else:
            rights = self.right_spinbox_1.value(), self.right_spinbox_2.value()
            lefts = self.left_spinbox_1.value(), self.left_spinbox_2.value()

            self.__new_model()

            for i in range(len(lefts)):
                self.model.shift_dots(i, 'right', rights[i])
                self.model.shift_dots(i, 'left', lefts[i])

        self.model.rebuild()

    def draw_optics(self) -> None:
        self.painter.draw_optic()
        self.canvas.draw()

        self.show_output()

    def draw_reflections(self) -> None:
        self.painter.draw_reflections()
        self.canvas.draw()

        self.show_output()

    def show_output(self) -> None:
        self.spot_out.setText(f'Spot on the target (mm): {self.model.calc_spot_radius()}')
        self.detector_out.setText(f'Spot on detector (mm): {self.model.calc_detector_size()}')
        self.angle_out.setText(f'Minimum angle (degrees): {self.model.calc_minimum_angle()}')

    def clear_output(self) -> None:
        self.spot_out.setText(f'Spot on the target (mm): ')
        self.detector_out.setText(f'Spot on detector (mm): ')
        self.angle_out.setText(f'Minimum angle (degrees): ')

    def change_view(self) -> None:
        self._is_vertical_view = not self._is_vertical_view

        self.axes.clear()
        self.canvas.draw()

        self.__new_model()
        self.do_shifts()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = GeomWindow()
    w.show()

    app.exec()
