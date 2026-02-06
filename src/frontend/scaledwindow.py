from backend.geometry import Geometry
from backend.painter import ScaledPainter

from frontend.spotwindow import SpotWindow
from frontend.settingswindow import SettingsWindow

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QMainWindow, QHBoxLayout, QVBoxLayout, QFrame, 
    QLabel, QDoubleSpinBox, QWidget, 
    QSlider, QTextEdit, QPushButton
)


class Ui_ScaledWindow(object):
    def setupUi(self, ScaledWindow):
        ScaledWindow.setObjectName("ScaledWindow")
        ScaledWindow.resize(1000, 750)
        ScaledWindow.setMinimumSize(QSize(1000, 750))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        ScaledWindow.setFont(font)
        self.centralwidget = QWidget(ScaledWindow)
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
        self.telescope1_layout = QVBoxLayout()
        self.telescope1_layout.setObjectName("telescope1_layout")
        self.telescope1_label = QLabel(self.tools_layout)
        self.telescope1_label.setAlignment(Qt.AlignCenter)
        self.telescope1_label.setObjectName("telescope1_label")
        self.telescope1_layout.addWidget(self.telescope1_label)
        self.telescope1_slider = QSlider(self.tools_layout)
        self.telescope1_slider.setMaximum(180)
        self.telescope1_slider.setOrientation(Qt.Horizontal)
        self.telescope1_slider.setObjectName("telescope1_slider")
        self.telescope1_slider.setRange(0, 180)
        self.telescope1_layout.addWidget(self.telescope1_slider)
        self.verticalLayout.addLayout(self.telescope1_layout)
        self.telescope2_layout = QVBoxLayout()
        self.telescope2_layout.setObjectName("telescope2_layout")
        self.telescope2_label = QLabel(self.tools_layout)
        self.telescope2_label.setAlignment(Qt.AlignCenter)
        self.telescope2_label.setObjectName("telescope2_label")
        self.telescope2_layout.addWidget(self.telescope2_label)
        self.telescope2_slider = QSlider(self.tools_layout)
        self.telescope2_slider.setMaximum(180)
        self.telescope2_slider.setOrientation(Qt.Horizontal)
        self.telescope2_slider.setObjectName("telescope2_slider")
        self.telescope2_slider.setRange(0, 180)
        self.telescope2_layout.addWidget(self.telescope2_slider)
        self.verticalLayout.addLayout(self.telescope2_layout)
        self.telescope3_layout = QVBoxLayout()
        self.telescope3_layout.setObjectName("telescope3_layout")
        self.telescope3_label = QLabel(self.tools_layout)
        self.telescope3_label.setAlignment(Qt.AlignCenter)
        self.telescope3_label.setObjectName("telescope3_label")
        self.telescope3_layout.addWidget(self.telescope3_label)
        self.telescope3_slider = QSlider(self.tools_layout)
        self.telescope3_slider.setOrientation(Qt.Horizontal)
        self.telescope3_slider.setObjectName("telescope3_slider")
        self.telescope3_slider.setRange(0, 24)
        self.telescope3_slider.setSingleStep(1)
        self.telescope3_slider.setTickInterval(1)
        self.telescope3_slider.setTickPosition(QSlider.TicksBelow)
        self.telescope3_layout.addWidget(self.telescope3_slider)
        self.verticalLayout.addLayout(self.telescope3_layout)
        self.target_layout = QVBoxLayout()
        self.target_layout.setObjectName("target_layout")
        self.target_label = QLabel(self.tools_layout)
        self.target_label.setAlignment(Qt.AlignCenter)
        self.target_label.setObjectName("target_label")
        self.target_layout.addWidget(self.target_label)
        self.target_slider = QSlider(self.tools_layout)
        self.target_slider.setRange(0, 8)
        self.target_slider.setValue(4)
        self.target_slider.setSingleStep(1)
        self.target_slider.setTickInterval(1)
        self.target_slider.setTickPosition(QSlider.TicksBelow)
        self.target_slider.setOrientation(Qt.Horizontal)
        self.target_slider.setObjectName("target_slider")
        self.target_layout.addWidget(self.target_slider)
        self.verticalLayout.addLayout(self.target_layout)
        self.remove_button = QPushButton(self.tools_layout)
        self.remove_button.setMinimumSize(QSize(0, 45))
        self.remove_button.setObjectName("remove_button")
        self.verticalLayout.addWidget(self.remove_button)
        self.settings_button = QPushButton(self.tools_layout)
        self.settings_button.setMinimumSize(QSize(0, 45))
        self.settings_button.setObjectName("settings_button")
        self.verticalLayout.addWidget(self.settings_button)
        self.output = QTextEdit(self.tools_layout)
        self.output.setObjectName("output")
        self.output.setReadOnly(True)
        self.verticalLayout.addWidget(self.output)
        self.collimator_optics_button = QPushButton(self.tools_layout)
        self.collimator_optics_button.setMinimumSize(QSize(0, 45))
        self.collimator_optics_button.setObjectName("collimator_optics_button")
        self.verticalLayout.addWidget(self.collimator_optics_button)
        self.telescope_optics_button = QPushButton(self.tools_layout)
        self.telescope_optics_button.setMinimumSize(QSize(0, 45))
        self.telescope_optics_button.setObjectName("telescope_optics_button")
        self.verticalLayout.addWidget(self.telescope_optics_button)
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
        ScaledWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ScaledWindow)
        QMetaObject.connectSlotsByName(ScaledWindow)

    def retranslateUi(self, ScaledWindow):
        _translate = QCoreApplication.translate
        ScaledWindow.setWindowTitle(_translate("ScaledWindow", "Geometry of Chamber"))
        self.h1_label.setText(_translate("ScaledWindow", "1st collim."))
        self.h1_box.setSuffix(_translate("ScaledWindow", " mm"))
        self.h2_label.setText(_translate("ScaledWindow", "2nd collim."))
        self.h2_box.setSuffix(_translate("ScaledWindow", " mm"))
        self.d1_label.setText(_translate("ScaledWindow", "D1:"))
        self.d1_box.setSuffix(_translate("ScaledWindow", " mm"))
        self.d2_label.setText(_translate("ScaledWindow", "D2:"))
        self.d2_box.setSuffix(_translate("ScaledWindow", " mm"))
        self.telescope1_label.setText(_translate("ScaledWindow", "1st telescope:"))
        self.telescope2_label.setText(_translate("ScaledWindow", "2nd telescope:"))
        self.telescope3_label.setText(_translate("ScaledWindow", "3rd telescope:"))
        self.target_label.setText(_translate("ScaledWindow", "Target angle:"))
        self.remove_button.setText(_translate("ScaledWindow", "Remove labels"))
        self.settings_button.setText(_translate("ScaledWindow", "Settings"))
        self.collimator_optics_button.setText(_translate("ScaledWindow", "Collimator optics"))
        self.telescope_optics_button.setText(_translate("ScaledWindow", "Telescope optics"))
        self.author_label.setText(_translate("ScaledWindow", "Chamber, LLENR app by TheKoke"))


class ScaledWindow(QMainWindow, Ui_ScaledWindow):
    def __init__(self, model: Geometry) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.mpl_connect('button_press_event', self.handle_click)
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        self.axes = self.view.figure.subplots()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.model = model
        self.painter = ScaledPainter(self.axes, model)
        self.setup_values()

        self.h1_box.valueChanged.connect(self.h1_change)
        self.h2_box.valueChanged.connect(self.h2_change)
        self.d1_box.valueChanged.connect(self.d1_change)
        self.d2_box.valueChanged.connect(self.d2_change)
        self.telescope1_slider.valueChanged.connect(self.telescope1_move)
        self.telescope2_slider.valueChanged.connect(self.telescope2_move)
        self.telescope3_slider.valueChanged.connect(self.telescope3_move)
        self.target_slider.valueChanged.connect(self.target_move)
        self.remove_button.clicked.connect(self.remove_labels)
        self.settings_button.clicked.connect(self.open_settings)
        self.collimator_optics_button.clicked.connect(self.collimator_optics_switch)
        self.telescope_optics_button.clicked.connect(self.telescope_optics_switch)

    def handle_click(self, event: MouseEvent) -> None:
        if event.dblclick and event.button == MouseButton.LEFT:
            pass

        if not event.dblclick and event.button == MouseButton.RIGHT:
            self.painter.draw()
            self.view.draw()

    def setup_values(self) -> None:
        h1 = self.model.chamber.ctube.first_collimator.diameter
        h2 = self.model.chamber.ctube.second_collimator.diameter
        d1 = self.model.chamber.ctube.second_collimator.x_position - self.model.chamber.ctube.first_collimator.x_position
        d2 = self.model.chamber.target.x_position - self.model.chamber.ctube.second_collimator.x_position

        theta1 = int(self.model.chamber.telescopes[0].theta)
        theta2 = int(self.model.chamber.telescopes[1].theta)
        theta3 = int(self.model.chamber.telescopes[2].theta)

        self.h1_box.setValue(h1)
        self.h2_box.setValue(h2)
        self.d1_box.setValue(d1)
        self.d2_box.setValue(d2)

        self.telescope1_slider.setValue(theta1)
        self.telescope2_slider.setValue(theta2)
        self.telescope3_slider.setValue(theta3)

        self.target_move()
        self.telescope1_move()
        self.telescope2_move()
        self.telescope3_move()

    def draw(self) -> None:
        self.painter.draw(autoscale=False)
        self.view.draw()

    def output(self) -> None:
        pass

    def h1_change(self) -> None:
        pass

    def h2_change(self) -> None:
        pass

    def d1_change(self) -> None:
        pass

    def d2_change(self) -> None:
        pass

    def telescope1_move(self) -> None:
        value = self.telescope1_slider.value()
        info = self.telescope1_label.text()
        new_info = info[:info.index(':')]

        new_info = new_info + f': {value} deg.'
        self.telescope1_label.setText(new_info)

        self.model.chamber.rotate_telescope(0, value)
        self.draw()

    def telescope2_move(self) -> None:
        value = self.telescope2_slider.value()
        info = self.telescope2_label.text()
        new_info = info[:info.index(':')]

        new_info = new_info + f': {value} deg.'
        self.telescope2_label.setText(new_info)

        self.model.chamber.rotate_telescope(1, value)
        self.draw()

    def telescope3_move(self) -> None:
        value = self.telescope3_slider.value()
        info = self.telescope3_label.text()
        new_info = info[:info.index(':')]

        new_info = new_info + f': {value} deg.'
        self.telescope3_label.setText(new_info)

        self.model.chamber.rotate_telescope(2, value)
        self.draw()

    def target_move(self) -> None:
        value = self.target_slider.value()
        info = self.target_label.text()
        new_info = info[:info.index(':')]

        step = 45
        ticks = 360 // step
        angle = (value - ticks // 2) * step

        new_info = new_info + f': {angle} deg.'
        self.target_label.setText(new_info)

        self.model.chamber.rotate_target(angle)
        self.draw()

    def remove_labels(self) -> None:
        self.painter.switch_labels()
        self.draw()

    def open_settings(self) -> None:
        self.settings = SettingsWindow(self.model.chamber)
        self.settings.show()

    def collimator_optics_switch(self) -> None:
        self.painter.switch_collimator_optics()
        self.draw()

    def telescope_optics_switch(self) -> None:
        self.painter.switch_telescope_optics()
        self.draw()


if __name__ == "__main__":
    pass
