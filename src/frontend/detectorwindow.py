from backend.environment import Detector

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, 
    QLabel, QDoubleSpinBox, QSpacerItem, 
    QSizePolicy, QDialogButtonBox, QDialog, QWidget
)


class Ui_DetectorWindow(object):
    def setupUi(self, DetectorWindow):
        DetectorWindow.setObjectName("DetectorWindow")
        DetectorWindow.resize(600, 300)
        DetectorWindow.setMinimumSize(QSize(600, 300))
        DetectorWindow.setMaximumSize(QSize(800, 450))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        DetectorWindow.setFont(font)
        self.horizontalLayout = QHBoxLayout(DetectorWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.coordiantes_layout = QFrame(DetectorWindow)
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
        self.horizontalLayout.addWidget(self.coordiantes_layout)
        self.info_layout = QFrame(DetectorWindow)
        self.info_layout.setFrameShape(QFrame.StyledPanel)
        self.info_layout.setFrameShadow(QFrame.Raised)
        self.info_layout.setObjectName("info_layout")
        self.verticalLayout_2 = QVBoxLayout(self.info_layout)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.detector_label = QLabel(self.info_layout)
        self.detector_label.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        font.setPointSize(20)
        self.detector_label.setFont(font)
        self.detector_label.setAlignment(Qt.AlignCenter)
        self.detector_label.setObjectName("detector_label")
        self.verticalLayout_2.addWidget(self.detector_label)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.okbutton = QDialogButtonBox(self.info_layout)
        self.okbutton.setMaximumSize(QSize(16777215, 50))
        self.okbutton.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.okbutton.setObjectName("okbutton")
        self.verticalLayout_2.addWidget(self.okbutton)
        self.horizontalLayout.addWidget(self.info_layout)

        self.retranslateUi(DetectorWindow)
        QMetaObject.connectSlotsByName(DetectorWindow)

    def retranslateUi(self, DetectorWindow):
        _translate = QCoreApplication.translate
        DetectorWindow.setWindowTitle(_translate("DetectorWindow", "Detector Settings"))
        self.xcoord_label.setText(_translate("DetectorWindow", "X:"))
        self.xcoord_box.setSuffix(_translate("DetectorWindow", " mm"))
        self.ycoord_label.setText(_translate("DetectorWindow", "Y:"))
        self.ycoord_box.setSuffix(_translate("DetectorWindow", " mm"))
        self.zcoord_label.setText(_translate("DetectorWindow", "Z:"))
        self.zcoord_box.setSuffix(_translate("DetectorWindow", " mm"))
        self.detector_label.setText(_translate("DetectorWindow", "Si-Detector"))


class DetectorWindow(QDialog, Ui_DetectorWindow):
    def __init__(self, detector: Detector) -> None:
        # window initializing
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./icon.ico'))

        # detector
        self.detector = detector

        # event handling
        ok, cancel = self.okbutton.buttons()
        ok.clicked.connect(self.save)
        cancel.clicked.connect(self.close)

    def save(self) -> None:
        xcoord = self.xcoord_box.value()
        ycoord = self.ycoord_box.value()
        zcoord = self.zcoord_box.value()

        dx = xcoord - self.detector.x_position
        dy = ycoord - self.detector.y_position
        dz = zcoord - self.detector.z_position

        self.detector.move(dx, dy, dz)


if __name__ == "__main__":
    pass
