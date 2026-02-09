from backend.geometry import Geometry
from backend.painter import UnscaledPainter

from frontend.spotwindow import SpotWindow
from frontend.targetwindow import TargetWindow
from frontend.detectorwindow import DetectorWindow
from frontend.collimatorwindow import CollimatorWindow

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFrame, QLabel, QDoubleSpinBox, QWidget, 
    QRadioButton, QTextEdit, QPushButton
)


class Ui_UnscaledWindow(object):
    def setupUi(self, UnscaledWindow):
        UnscaledWindow.setObjectName("UnscaledWindow")
        UnscaledWindow.resize(1000, 750)
        UnscaledWindow.setMinimumSize(QSize(1000, 750))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        UnscaledWindow.setFont(font)
        self.centralwidget = QWidget(UnscaledWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tools_layout = QFrame(self.centralwidget)
        self.tools_layout.setMinimumSize(QSize(200, 0))
        self.tools_layout.setMaximumSize(QSize(350, 16777215))
        self.tools_layout.setFrameShape(QFrame.StyledPanel)
        self.tools_layout.setFrameShadow(QFrame.Raised)
        self.tools_layout.setObjectName("tools_layout")
        self.verticalLayout = QVBoxLayout(self.tools_layout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.h1_layout = QHBoxLayout()
        self.h1_layout.setObjectName("h1_layout")
        self.h1_label = QLabel(self.tools_layout)
        self.h1_label.setObjectName("h1_label")
        self.h1_layout.addWidget(self.h1_label)
        self.h1_box = QDoubleSpinBox(self.tools_layout)
        self.h1_box.setSingleStep(0.01)
        self.h1_box.setProperty("value", 1.0)
        self.h1_box.setObjectName("h1_box")
        self.h1_layout.addWidget(self.h1_box)
        self.verticalLayout.addLayout(self.h1_layout)
        self.h2_layout = QHBoxLayout()
        self.h2_layout.setObjectName("h2_layout")
        self.h2_label = QLabel(self.tools_layout)
        self.h2_label.setObjectName("h2_label")
        self.h2_layout.addWidget(self.h2_label)
        self.h2_box = QDoubleSpinBox(self.tools_layout)
        self.h2_box.setSingleStep(0.01)
        self.h2_box.setProperty("value", 1.0)
        self.h2_box.setObjectName("h2_box")
        self.h2_layout.addWidget(self.h2_box)
        self.verticalLayout.addLayout(self.h2_layout)
        self.d1_layout = QHBoxLayout()
        self.d1_layout.setObjectName("d1_layout")
        self.d1_label = QLabel(self.tools_layout)
        self.d1_label.setObjectName("d1_label")
        self.d1_layout.addWidget(self.d1_label)
        self.d1_box = QDoubleSpinBox(self.tools_layout)
        self.d1_box.setMaximum(99999.99)
        self.d1_box.setSingleStep(0.01)
        self.d1_box.setProperty("value", 100.0)
        self.d1_box.setObjectName("d1_box")
        self.d1_layout.addWidget(self.d1_box)
        self.verticalLayout.addLayout(self.d1_layout)
        self.d2_layout = QHBoxLayout()
        self.d2_layout.setObjectName("d2_layout")
        self.d2_label = QLabel(self.tools_layout)
        self.d2_label.setObjectName("d2_label")
        self.d2_layout.addWidget(self.d2_label)
        self.d2_box = QDoubleSpinBox(self.tools_layout)
        self.d2_box.setMaximum(99999.99)
        self.d2_box.setSingleStep(0.01)
        self.d2_box.setProperty("value", 100.0)
        self.d2_box.setObjectName("d2_box")
        self.d2_layout.addWidget(self.d2_box)
        self.verticalLayout.addLayout(self.d2_layout)
        self.d3_layout = QHBoxLayout()
        self.d3_layout.setObjectName("d3_layout")
        self.d3_label = QLabel(self.tools_layout)
        self.d3_label.setObjectName("d3_label")
        self.d3_layout.addWidget(self.d3_label)
        self.d3_box = QDoubleSpinBox(self.tools_layout)
        self.d3_box.setMaximum(99999.99)
        self.d3_box.setSingleStep(0.01)
        self.d3_box.setProperty("value", 100.0)
        self.d3_box.setObjectName("d3_box")
        self.d3_layout.addWidget(self.d3_box)
        self.verticalLayout.addLayout(self.d3_layout)
        self.collimator1_button = QPushButton(self.tools_layout)
        self.collimator1_button.setMinimumSize(QSize(0, 45))
        self.collimator1_button.setObjectName("collimator1_button")
        self.verticalLayout.addWidget(self.collimator1_button)
        self.collimator2_button = QPushButton(self.tools_layout)
        self.collimator2_button.setMinimumSize(QSize(0, 45))
        self.collimator2_button.setObjectName("collimator2_button")
        self.verticalLayout.addWidget(self.collimator2_button)
        self.target_button = QPushButton(self.tools_layout)
        self.target_button.setMinimumSize(QSize(0, 45))
        self.target_button.setObjectName("target_button")
        self.verticalLayout.addWidget(self.target_button)
        self.detector_button = QPushButton(self.tools_layout)
        self.detector_button.setMinimumSize(QSize(0, 45))
        self.detector_button.setObjectName("detector_button")
        self.verticalLayout.addWidget(self.detector_button)
        self.plane_layout = QHBoxLayout()
        self.plane_layout.setObjectName("plane_layout")
        self.xy_radio = QRadioButton(self.tools_layout)
        self.xy_radio.setObjectName("xy_radio")
        self.plane_layout.addWidget(self.xy_radio)
        self.xz_radio = QRadioButton(self.tools_layout)
        self.xz_radio.setObjectName("xz_radio")
        self.plane_layout.addWidget(self.xz_radio)
        self.verticalLayout.addLayout(self.plane_layout)
        self.output = QTextEdit(self.tools_layout)
        self.output.setObjectName("output")
        self.output.setReadOnly(True)
        self.verticalLayout.addWidget(self.output)
        self.optics_button = QPushButton(self.tools_layout)
        self.optics_button.setMinimumSize(QSize(0, 45))
        self.optics_button.setObjectName("optics_button")
        self.verticalLayout.addWidget(self.optics_button)
        self.reflections_button = QPushButton(self.tools_layout)
        self.reflections_button.setMinimumSize(QSize(0, 45))
        self.reflections_button.setObjectName("reflections_button")
        self.verticalLayout.addWidget(self.reflections_button)
        self.spot_button = QPushButton(self.tools_layout)
        self.spot_button.setMinimumSize(QSize(0, 60))
        self.spot_button.setObjectName("spot_button")
        self.verticalLayout.addWidget(self.spot_button)
        self.author_label = QLabel(self.tools_layout)
        font = QFont()
        font.setPointSize(9)
        self.author_label.setFont(font)
        self.author_label.setAlignment(Qt.AlignCenter)
        self.author_label.setWordWrap(True)
        self.author_label.setObjectName("author_label")
        self.verticalLayout.addWidget(self.author_label)
        self.horizontalLayout.addWidget(self.tools_layout)
        self.matplotlib_layout = QFrame(self.centralwidget)
        self.matplotlib_layout.setMinimumSize(QSize(780, 0))
        self.matplotlib_layout.setFrameShape(QFrame.StyledPanel)
        self.matplotlib_layout.setFrameShadow(QFrame.Raised)
        self.matplotlib_layout.setObjectName("matplotlib_layout")
        self.horizontalLayout.addWidget(self.matplotlib_layout)
        UnscaledWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UnscaledWindow)
        QMetaObject.connectSlotsByName(UnscaledWindow)

    def retranslateUi(self, UnscaledWindow):
        _translate = QCoreApplication.translate
        UnscaledWindow.setWindowTitle(_translate("UnscaledWindow", "Geometry of Chamber"))
        self.h1_label.setText(_translate("UnscaledWindow", "1st collim."))
        self.h1_box.setSuffix(_translate("UnscaledWindow", " mm"))
        self.h2_label.setText(_translate("UnscaledWindow", "2nd collim."))
        self.h2_box.setSuffix(_translate("UnscaledWindow", " mm"))
        self.d1_label.setText(_translate("UnscaledWindow", "D1:"))
        self.d1_box.setSuffix(_translate("UnscaledWindow", " mm"))
        self.d2_label.setText(_translate("UnscaledWindow", "D2:"))
        self.d2_box.setSuffix(_translate("UnscaledWindow", " mm"))
        self.d3_label.setText(_translate("UnscaledWindow", "D3:"))
        self.d3_box.setSuffix(_translate("UnscaledWindow", " mm"))
        self.collimator1_button.setText(_translate("UnscaledWindow", "1st Collimator Settings"))
        self.collimator2_button.setText(_translate("UnscaledWindow", "2nd Collimator Settings"))
        self.target_button.setText(_translate("UnscaledWindow", "Target Settings"))
        self.detector_button.setText(_translate("UnscaledWindow", "Detector Settings"))
        self.xy_radio.setText(_translate("UnscaledWindow", "XY-Plane"))
        self.xz_radio.setText(_translate("UnscaledWindow", "XZ-Plane"))
        self.optics_button.setText(_translate("UnscaledWindow", "Optics"))
        self.reflections_button.setText(_translate("UnscaledWindow", "Reflections"))
        self.spot_button.setText(_translate("UnscaledWindow", "Spot on Target"))
        self.author_label.setText(_translate("UnscaledWindow", "Chamber, LLENR app by TheKoke"))


class UnscaledWindow(QMainWindow, Ui_UnscaledWindow):
    def __init__(self, model: Geometry) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.mpl_connect('button_press_event', self.add_pointer)
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        self.axes = self.view.figure.subplots()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.model = model
        self.painter = UnscaledPainter(self.axes, model)
        self.setup_values()
        self.show_output()

        self.h1_box.valueChanged.connect(self.h1_change)
        self.h2_box.valueChanged.connect(self.h2_change)
        self.d1_box.valueChanged.connect(self.d1_change)
        self.d2_box.valueChanged.connect(self.d2_change)
        self.d3_box.valueChanged.connect(self.d3_change)
        self.collimator1_button.clicked.connect(self.open_collimator1)
        self.collimator2_button.clicked.connect(self.open_collimator2)
        self.target_button.clicked.connect(self.open_target)
        self.detector_button.clicked.connect(self.open_detector)
        self.optics_button.clicked.connect(self.switch_optics)
        self.reflections_button.clicked.connect(self.switch_reflections)
        self.spot_button.clicked.connect(self.open_spot)

        self.xy_radio.setChecked(True)
        self.xy_radio.clicked.connect(self.xy_plane)
        self.xz_radio.clicked.connect(self.xz_plane)

    def add_pointer(self, event: MouseEvent) -> None:
        pass

    def setup_values(self) -> None:
        h1 = self.model.chamber.ctube.first_collimator.diameter
        h2 = self.model.chamber.ctube.second_collimator.diameter

        d1 = self.model.chamber.ctube.length
        d2 = self.model.chamber.target.x_position - self.model.chamber.ctube.second_collimator.x_position
        d3 = self.model.chamber.telescopes[0].detector.x_position - self.model.chamber.target.x_position

        self.h1_box.setValue(h1)
        self.h2_box.setValue(h2)
        self.d1_box.setValue(d1)
        self.d2_box.setValue(d2)
        self.d3_box.setValue(d3)

    def refresh(self) -> None:
        self.painter.draw(self.painter.current_plane)
        self.view.draw()
        self.show_output()
        self.setup_values()

    def show_output(self) -> None:
        output = f'Spot on Target: {round(self.model.spot_on_target(), 3)} mm\n\n'
        output += f'Spot on Detector: {round(self.model.spot_on_detector()[0], 3)} mm\n\n'
        output += f'Angle resolution: {round(self.model.angle_resolution()[0], 3)} deg.\n\n'

        self.output.setText(output)

    def h1_change(self) -> None:
        new = self.h1_box.value()
        if new <= 0.0:
            return
        
        self.model.chamber.ctube.first_collimator.diameter = new
        self.refresh()

    def h2_change(self) -> None:
        new = self.h2_box.value()
        if new <= 0.0:
            return
        
        self.model.chamber.ctube.second_collimator.diameter = new
        self.refresh()

    def d1_change(self) -> None:
        new = self.d1_box.value()
        if new <= 0.0:
            return
        
        self.model.chamber.change_ctube_length(new)
        self.refresh()

    def d2_change(self) -> None:
        new = self.d2_box.value()
        if new <= 0.0:
            return
        
        self.model.chamber.move_ctube(new)
        self.refresh()

    def d3_change(self) -> None:
        new = self.d3_box.value()
        if new <= 0.0:
            return
        
        old = self.model.chamber.telescopes[0].detector.x_position - self.model.chamber.target.x_position
        self.model.chamber.telescopes[0].move(new - old, 0, 0)
        self.refresh()

    def open_collimator1(self) -> None:
        self.opened = CollimatorWindow(self.model.chamber.ctube.first_collimator)
        self.opened.okbutton.buttons()[0].clicked.connect(self.refresh)
        self.opened.okbutton.buttons()[1].clicked.connect(self.refresh)
        self.opened.show()
    
    def open_collimator2(self) -> None:
        self.opened = CollimatorWindow(self.model.chamber.ctube.second_collimator)
        self.opened.okbutton.buttons()[0].clicked.connect(self.refresh)
        self.opened.okbutton.buttons()[1].clicked.connect(self.refresh)
        self.opened.show()

    def open_target(self) -> None:
        self.opened = TargetWindow(self.model.chamber.target)
        self.opened.okbutton.buttons()[0].clicked.connect(self.refresh)
        self.opened.okbutton.buttons()[1].clicked.connect(self.refresh)
        self.opened.show()

    def open_detector(self) -> None:
        self.opened = DetectorWindow(self.model.chamber.telescopes[0].detector)
        self.opened.okbutton.buttons()[0].clicked.connect(self.refresh)
        self.opened.okbutton.buttons()[1].clicked.connect(self.refresh)
        self.opened.show()

    def xy_plane(self) -> None:
        self.painter.draw('xy')
        self.view.draw()

    def xz_plane(self) -> None:
        self.painter.draw('xz')
        self.view.draw()

    def switch_optics(self) -> None:
        self.painter.switch_optics()
        self.view.draw()

    def switch_reflections(self) -> None:
        self.painter.switch_reflections()
        self.view.draw()

    def open_spot(self) -> None:
        self.opened = SpotWindow(self.model)
        self.opened.show()


if __name__ == "__main__":
    pass
