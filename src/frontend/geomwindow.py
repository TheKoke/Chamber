from backend.painter import UnscaledPainter
from backend.geometry import Geometry

from frontend.spotwindow import SpotWindow
from frontend.targetwindow import TargetWindow
# from frontend.detectorwindow import DetectorWindow
from frontend.collimatorwindow import CollimatorWindow

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, 
    QFrame, QLabel, QTextEdit, QPushButton, QRadioButton
)

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg


class Ui_GeomWindow(object):
    def setupUi(self, GeomWindow):
        GeomWindow.setObjectName("GeomWindow")
        GeomWindow.resize(1000, 750)
        GeomWindow.setMinimumSize(QSize(1000, 750))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        GeomWindow.setFont(font)
        self.centralwidget = QWidget(GeomWindow)
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
        self.collimator1_button = QPushButton(self.tools_layout)
        self.collimator1_button.setMinimumSize(QSize(0, 50))
        self.collimator1_button.setObjectName("collimator1_button")
        self.verticalLayout.addWidget(self.collimator1_button)
        self.collimator2_button = QPushButton(self.tools_layout)
        self.collimator2_button.setMinimumSize(QSize(0, 50))
        self.collimator2_button.setObjectName("collimator2_button")
        self.verticalLayout.addWidget(self.collimator2_button)
        self.target_button = QPushButton(self.tools_layout)
        self.target_button.setMinimumSize(QSize(0, 50))
        self.target_button.setObjectName("target_button")
        self.verticalLayout.addWidget(self.target_button)
        self.detector_button = QPushButton(self.tools_layout)
        self.detector_button.setMinimumSize(QSize(0, 50))
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
        self.optics_button.setMinimumSize(QSize(0, 50))
        self.optics_button.setObjectName("optics_button")
        self.verticalLayout.addWidget(self.optics_button)
        self.reflections_button = QPushButton(self.tools_layout)
        self.reflections_button.setMinimumSize(QSize(0, 50))
        self.reflections_button.setObjectName("reflections_button")
        self.verticalLayout.addWidget(self.reflections_button)
        self.spot_button = QPushButton(self.tools_layout)
        self.spot_button.setMinimumSize(QSize(0, 65))
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
        GeomWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(GeomWindow)
        QMetaObject.connectSlotsByName(GeomWindow)

    def retranslateUi(self, GeomWindow):
        _translate = QCoreApplication.translate
        GeomWindow.setWindowTitle(_translate("GeomWindow", "Geometry of Chamber"))
        self.collimator1_button.setText(_translate("GeomWindow", "1st Collimator Settings"))
        self.collimator2_button.setText(_translate("GeomWindow", "2nd Collimator Settings"))
        self.target_button.setText(_translate("GeomWindow", "Target Settings"))
        self.detector_button.setText(_translate("GeomWindow", "Detector Settings"))
        self.xy_radio.setText(_translate("GeomWindow", "XY-Plane"))
        self.xz_radio.setText(_translate("GeomWindow", "XZ-Plane"))
        self.optics_button.setText(_translate("GeomWindow", "Optics"))
        self.reflections_button.setText(_translate("GeomWindow", "Reflections"))
        self.spot_button.setText(_translate("GeomWindow", "Spot on Target"))
        self.author_label.setText(_translate("GeomWindow", "Chamber, LLENR app by TheKoke"))


class GeomWindow(QMainWindow, Ui_GeomWindow):
    def __init__(self, model: Geometry) -> None:
        # window initializing
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./icon.ico'))

        # matplotlib
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.mpl_connect('button_press_event', self.add_pointer)
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        # model, painter and pointer
        self.model = model
        self.paint = UnscaledPainter(self.axes, model)
        self.pointer = None

        # event handling
        self.collimator1_button.clicked.connect(self.open_first_collimator)
        self.collimator2_button.clicked.connect(self.open_last_collimator)
        self.target_button.clicked.connect(self.open_target)
        # self.detector_button.clicked.connect(self.open_detector)
        self.optics_button.clicked.connect(self.switch_optics)
        self.reflections_button.clicked.connect(self.switch_reflections)
        self.spot_button.clicked.connect(self.look_at_spot)

        self.xy_radio.setChecked(True)
        self.xy_radio.clicked.connect(self.xy_plane)
        self.xz_radio.clicked.connect(self.xz_plane)

        self.show_output()

    def add_pointer(self, event: MouseEvent) -> None:
        if event.dblclick:
            pass

    def show_output(self) -> None:
        output = f'Spot on Target: {round(self.model.spot_on_target(), 3)} mm\n\n'
        output += f'Spot on Detector: {round(self.model.spot_on_detector(), 3)} mm\n\n'
        output += f'Angle resolution: {round(self.model.angle_resolution(), 3)} deg.\n\n'

        if self.pointer is not None:
            output += f'Cutting Collimator Radius must be: {round(self.model.spot_at_distance(self.pointer), 3)}'

        self.output.setText(output)

    def xy_plane(self) -> None:
        self.paint.draw('xy')
        self.view.draw()

    def xz_plane(self) -> None:
        self.paint.draw('xz')
        self.view.draw()

    def switch_optics(self) -> None:
        self.paint.switch_optics()
        self.view.draw()

    def switch_reflections(self) -> None:
        self.paint.switch_reflections()
        self.view.draw()

    def open_first_collimator(self) -> None:
        self._window = CollimatorWindow(self.model.first_collimator)
        self._window.okbutton.buttons()[0].clicked.connect(self.refresh)
        self._window.show()

    def open_last_collimator(self) -> None:
        self._window = CollimatorWindow(self.model.last_collimator)
        self._window.okbutton.buttons()[0].clicked.connect(self.refresh)
        self._window.show()

    def open_target(self) -> None:
        self._window = TargetWindow(self.model.target)
        self._window.okbutton.buttons()[0].clicked.connect(self.refresh)
        self._window.show()

    def open_detector(self) -> None:
        # self._window = DetectorWindow(self.model.detector)
        self._window.okbutton.buttons()[0].clicked.connect(self.refresh)
        self._window.show()

    def look_at_spot(self) -> None:
        self._window = SpotWindow(self.model)
        self._window.show()

    def refresh(self) -> None:
        self.show_output()

        self.paint.draw(self.paint.current_plane)
        self.view.draw()


if __name__ == '__main__':
    pass
