from backend.environment import Telescope
from frontend.collimatorwindow import CollimatorWindow

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, 
    QLabel, QDoubleSpinBox, QSpacerItem, 
    QSizePolicy, QDialogButtonBox, QDialog, QPushButton
)


class Ui_TelescopeWindow(object):
    def setupUi(self, TelescopeWindow):
        TelescopeWindow.setObjectName("TelescopeWindow")
        TelescopeWindow.resize(600, 300)
        TelescopeWindow.setMinimumSize(QSize(600, 300))
        TelescopeWindow.setMaximumSize(QSize(800, 450))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        TelescopeWindow.setFont(font)
        self.horizontalLayout = QHBoxLayout(TelescopeWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.coordiantes_layout = QFrame(TelescopeWindow)
        self.coordiantes_layout.setFrameShape(QFrame.StyledPanel)
        self.coordiantes_layout.setFrameShadow(QFrame.Raised)
        self.coordiantes_layout.setObjectName("coordiantes_layout")
        self.verticalLayout = QVBoxLayout(self.coordiantes_layout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.xcoord_layout = QHBoxLayout()
        self.xcoord_layout.setObjectName("xcoord_layout")
        self.xcoord_label = QLabel(self.coordiantes_layout)
        self.xcoord_label.setMaximumSize(QSize(16777215, 40))
        self.xcoord_label.setAlignment(Qt.AlignCenter)
        self.xcoord_label.setObjectName("xcoord_label")
        self.xcoord_layout.addWidget(self.xcoord_label)
        self.xcoord_box = QDoubleSpinBox(self.coordiantes_layout)
        self.xcoord_box.setMaximum(999999999.0)
        self.xcoord_box.setSingleStep(0.1)
        self.xcoord_box.setObjectName("xcoord_box")
        self.xcoord_layout.addWidget(self.xcoord_box)
        self.verticalLayout.addLayout(self.xcoord_layout)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.ycoord_layout = QHBoxLayout()
        self.ycoord_layout.setObjectName("ycoord_layout")
        self.ycoord_label = QLabel(self.coordiantes_layout)
        self.ycoord_label.setMaximumSize(QSize(16777215, 40))
        self.ycoord_label.setAlignment(Qt.AlignCenter)
        self.ycoord_label.setObjectName("ycoord_label")
        self.ycoord_layout.addWidget(self.ycoord_label)
        self.ycoord_box = QDoubleSpinBox(self.coordiantes_layout)
        self.ycoord_box.setMaximum(999999999.0)
        self.ycoord_box.setSingleStep(0.1)
        self.ycoord_box.setObjectName("ycoord_box")
        self.ycoord_layout.addWidget(self.ycoord_box)
        self.verticalLayout.addLayout(self.ycoord_layout)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.zcoord_layout = QHBoxLayout()
        self.zcoord_layout.setObjectName("zcoord_layout")
        self.zcoord_label = QLabel(self.coordiantes_layout)
        self.zcoord_label.setMaximumSize(QSize(16777215, 40))
        self.zcoord_label.setAlignment(Qt.AlignCenter)
        self.zcoord_label.setObjectName("zcoord_label")
        self.zcoord_layout.addWidget(self.zcoord_label)
        self.zcoord_box = QDoubleSpinBox(self.coordiantes_layout)
        self.zcoord_box.setMaximum(999999999.0)
        self.zcoord_box.setSingleStep(0.1)
        self.zcoord_box.setObjectName("zcoord_box")
        self.zcoord_layout.addWidget(self.zcoord_box)
        self.verticalLayout.addLayout(self.zcoord_layout)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.angle_layout = QHBoxLayout()
        self.angle_layout.setObjectName("angle_layout")
        self.angle_label = QLabel(self.coordiantes_layout)
        self.angle_label.setMaximumSize(QSize(15, 40))
        self.angle_label.setAlignment(Qt.AlignCenter)
        self.angle_label.setObjectName("angle_label")
        self.angle_layout.addWidget(self.angle_label)
        self.angle_box = QDoubleSpinBox(self.coordiantes_layout)
        self.angle_box.setAccelerated(True)
        self.angle_box.setMaximum(180.0)
        self.angle_box.setSingleStep(0.01)
        self.angle_box.setObjectName("angle_box")
        self.angle_layout.addWidget(self.angle_box)
        self.verticalLayout.addLayout(self.angle_layout)
        self.horizontalLayout.addWidget(self.coordiantes_layout)
        self.info_layout = QFrame(TelescopeWindow)
        self.info_layout.setFrameShape(QFrame.StyledPanel)
        self.info_layout.setFrameShadow(QFrame.Raised)
        self.info_layout.setObjectName("info_layout")
        self.verticalLayout_2 = QVBoxLayout(self.info_layout)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.info_label = QLabel(self.info_layout)
        self.info_label.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        font.setPointSize(20)
        self.info_label.setFont(font)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setObjectName("info_label")
        self.verticalLayout_2.addWidget(self.info_label)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.collimators_layout = QHBoxLayout()
        self.collimators_layout.setObjectName("collimators_layout")
        self.first_button = QPushButton(self.info_layout)
        self.first_button.setMinimumSize(QSize(0, 50))
        self.first_button.setObjectName("first_button")
        self.collimators_layout.addWidget(self.first_button)
        self.second_button = QPushButton(self.info_layout)
        self.second_button.setMinimumSize(QSize(0, 50))
        self.second_button.setObjectName("second_button")
        self.collimators_layout.addWidget(self.second_button)
        self.verticalLayout_2.addLayout(self.collimators_layout)
        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.okbutton = QDialogButtonBox(self.info_layout)
        self.okbutton.setMaximumSize(QSize(16777215, 50))
        self.okbutton.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.okbutton.setObjectName("okbutton")
        self.verticalLayout_2.addWidget(self.okbutton)
        self.horizontalLayout.addWidget(self.info_layout)

        self.retranslateUi(TelescopeWindow)
        QMetaObject.connectSlotsByName(TelescopeWindow)

    def retranslateUi(self, TelescopeWindow):
        _translate = QCoreApplication.translate
        TelescopeWindow.setWindowTitle(_translate("TelescopeWindow", "Telescope Settings"))
        self.xcoord_label.setText(_translate("TelescopeWindow", "X:"))
        self.xcoord_box.setSuffix(_translate("TelescopeWindow", " mm"))
        self.ycoord_label.setText(_translate("TelescopeWindow", "Y:"))
        self.ycoord_box.setSuffix(_translate("TelescopeWindow", " mm"))
        self.zcoord_label.setText(_translate("TelescopeWindow", "Z:"))
        self.zcoord_box.setSuffix(_translate("TelescopeWindow", " mm"))
        self.angle_label.setText(_translate("TelescopeWindow", "α:"))
        self.angle_box.setSuffix(_translate("TelescopeWindow", " deg."))
        self.info_label.setText(_translate("TelescopeWindow", "E-dE Telescope"))
        self.first_button.setText(_translate("TelescopeWindow", "1st collimator"))
        self.second_button.setText(_translate("TelescopeWindow", "2nd collimator"))


class TelescopeWindow(QDialog, Ui_TelescopeWindow):
    def __init__(self, telescope: Telescope) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        self.telescope = telescope

        self.first_button.clicked.connect(self.open_first)
        self.second_button.clicked.connect(self.open_second)

    def open_first(self) -> None:
        self.collim_window = CollimatorWindow(self.telescope.first_collimator)
        self.collim_window.show()
        return

    def open_second(self) -> None:
        self.collim_window = CollimatorWindow(self.telescope.second_collimator)
        self.collim_window.show()
        return


if __name__ == "__main__":
    pass
