import sys

from back import *
from front import Ui_MainWindow
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg


class SpotWindow(QWidget):
    def __init__(self, r1: float, r2: float, shift_x: float, shift_y: float) -> None:
        super().__init__()

        self.r1 = r1
        self.r2 = r2
        self.shift_x = shift_x
        self.shift_y = shift_y

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
        draw_ellipse(self.axes, self.r1, self.r2, self.shift_x, self.shift_y)

        self.axes.set_ylim(-20, 20)
        self.axes.set_xlim((-20, 20))
        self.axes.set_aspect('equal')
        self.axes.legend()


class GeomWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.setMinimumSize(1300, 900)
        self.size_grip = QSizeGrip(self)

        self._is_vertical_view = True

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(20, 17)))
        self.axes = self.canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        mask = QVBoxLayout(self.matplotlib_layout)

        mask.addWidget(self.toolbar)
        mask.addWidget(self.canvas)

        d1, d2, d3 = self.d1_box.value(), self.d2_box.value(), self.d3_box.value()
        h1, h2 = self.r1_box.value(), self.r2_box.value()
        t1, t2 = self.t1_box.value(), self.t2_box.value()

        self.model = Geometry(h1, h2, d1, d2, d3, t1, t2, 'v' if self._is_vertical_view else 'h')
        self.painter = Painter(self.axes, self.model)

        # general properties
        self.d1_box.valueChanged.connect(self.prop_change)
        self.d2_box.valueChanged.connect(self.prop_change)
        self.d3_box.valueChanged.connect(self.prop_change)
        self.r1_box.valueChanged.connect(self.prop_change)
        self.r2_box.valueChanged.connect(self.prop_change)
        self.t1_box.valueChanged.connect(self.prop_change)
        self.t2_box.valueChanged.connect(self.prop_change)

        # tilting properties
        self.v_1.valueChanged.connect(self.tilt_change)
        self.v_2.valueChanged.connect(self.tilt_change)
        self.h_1.valueChanged.connect(self.tilt_change)
        self.h_2.valueChanged.connect(self.tilt_change)

        # general buttons
        self.optics_button.clicked.connect(self.draw_optics)
        self.reflections_button.clicked.connect(self.draw_reflections)
        self.view_button.clicked.connect(self.change_view)
        self.spot_button.clicked.connect(self.look_at_spot)

        self.show()

    def __new_model(self) -> None:
        self.__check_params()

        d1, d2, d3 = self.d1_box.value(), self.d2_box.value(), self.d3_box.value()
        h1, h2 = self.r1_box.value(), self.r2_box.value()
        t1, t2 = self.t1_box.value(), self.t2_box.value()

        self.model = Geometry(h1, h2, d1, d2, d3, t1, t2, 'v' if self._is_vertical_view else 'h')
        self.painter = Painter(self.axes, self.model)

    def __check_params(self) -> None:
        #                  d1   d2   d3   h1   h2   t1   t2
        default_params = [960, 360, 220, 3.0, 3.0, 2.0, 2.0]

        current_params = [
            self.d1_box.value(), self.d2_box.value(), self.d3_box.value(),
            self.r1_box.value(), self.r2_box.value(),
            self.t1_box.value(), self.t2_box.value()
        ]

        matched_spinboxes = [
            self.d1_box, self.d2_box, self.d3_box, self.r1_box, self.r2_box,
            self.t1_box, self.t2_box
        ]

        for i in range(len(current_params)):
            if current_params[i] == 0:
                matched_spinboxes[i].setValue(default_params[i])

    def look_at_spot(self) -> None:
        v1, v2 = self.v_1.value(), self.v_2.value()
        h1, h2 = self.h_1.value(), self.h_2.value()

        x_shift = h2 - h1
        y_shift = v2 - v1

        self.window = SpotWindow(self.r1_box.value(), self.r2_box.value(), x_shift, y_shift)
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
        v1, v2 = self.v_1.value(), self.v_2.value()
        h1, h2 = self.h_1.value(), self.h_2.value()

        self.__new_model()

        self.model.shift_dots(0, 'vertical', v1)
        self.model.shift_dots(0, 'horizonthal', h1)
        self.model.shift_dots(1, 'vertical', v2)
        self.model.shift_dots(1, 'horizonthal', h2)

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
        self.spot_out.setText(f'Spot on the target (mm): {round(self.model.calc_spot_radius(), 3)}')
        self.detector_out.setText(f'Spot on detector (mm): {round(self.model.calc_detector_size(), 3)}')
        self.angle_out.setText(f'Minimum angle (degrees): {round(self.model.calc_minimum_angle(), 3)}')
        self.cutting_out.setText(f'Cutting collim. radius (mm):')

    def clear_output(self) -> None:
        self.spot_out.setText(f'Spot on the target (mm): ')
        self.detector_out.setText(f'Spot on detector (mm): ')
        self.angle_out.setText(f'Minimum angle (degrees): ')
        self.cutting_out.setText(f'Cutting collim. radius (mm):')

    def change_view(self) -> None:
        self._is_vertical_view = not self._is_vertical_view

        self.axes.clear()
        self.canvas.draw()

        self.__new_model()
        self.do_shifts()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GeomWindow()
    app.exec()
