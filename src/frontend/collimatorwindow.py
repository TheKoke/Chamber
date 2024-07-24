from backend.environment import Collimator

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, 
    QLabel, QDoubleSpinBox, QSpacerItem, 
    QSizePolicy, QDialogButtonBox, QDialog
)


class Ui_CollimatorWindow(object):
    def setupUi(self, DetectorWindow):
        DetectorWindow.setObjectName("CollimatorWindow")
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
        self.xcoord_box.setMinimum(-999999999.0)
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
        self.ycoord_box.setMinimum(-999999999.0)
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
        self.zcoord_box.setMinimum(-999999999.0)
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
        self.collimator_label = QLabel(self.info_layout)
        self.collimator_label.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        font.setPointSize(20)
        self.collimator_label.setFont(font)
        self.collimator_label.setAlignment(Qt.AlignCenter)
        self.collimator_label.setObjectName("collimator_label")
        self.verticalLayout_2.addWidget(self.collimator_label)
        self.properties_label = QLabel(self.info_layout)
        self.properties_label.setAlignment(Qt.AlignCenter)
        self.properties_label.setObjectName("properties_label")
        self.verticalLayout_2.addWidget(self.properties_label)
        self.properties_layout = QHBoxLayout()
        self.properties_layout.setObjectName("properties_layout")
        self.radius_layout = QHBoxLayout()
        self.radius_layout.setObjectName("radius_layout")
        self.radius_label = QLabel(self.info_layout)
        self.radius_label.setMaximumSize(QSize(16777215, 40))
        self.radius_label.setAlignment(Qt.AlignCenter)
        self.radius_label.setObjectName("radius_label")
        self.radius_layout.addWidget(self.radius_label)
        self.radius_box = QDoubleSpinBox(self.info_layout)
        self.radius_box.setMaximum(999999999.0)
        self.radius_box.setSingleStep(0.1)
        self.radius_box.setProperty("value", 3.0)
        self.radius_box.setObjectName("radius_box")
        self.radius_layout.addWidget(self.radius_box)
        self.properties_layout.addLayout(self.radius_layout)
        self.thickness_layout = QHBoxLayout()
        self.thickness_layout.setObjectName("thickness_layout")
        self.thickness_label = QLabel(self.info_layout)
        self.thickness_label.setMaximumSize(QSize(16777215, 40))
        self.thickness_label.setAlignment(Qt.AlignCenter)
        self.thickness_label.setObjectName("thickness_label")
        self.thickness_layout.addWidget(self.thickness_label)
        self.thickness_box = QDoubleSpinBox(self.info_layout)
        self.thickness_box.setMaximum(999999999.0)
        self.thickness_box.setSingleStep(0.1)
        self.thickness_box.setProperty("value", 2.0)
        self.thickness_box.setObjectName("thickness_box")
        self.thickness_layout.addWidget(self.thickness_box)
        self.properties_layout.addLayout(self.thickness_layout)
        self.verticalLayout_2.addLayout(self.properties_layout)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.okbutton = QDialogButtonBox(self.info_layout)
        self.okbutton.setMaximumSize(QSize(16777215, 50))
        self.okbutton.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.okbutton.setObjectName("okbutton")
        self.verticalLayout_2.addWidget(self.okbutton)
        self.horizontalLayout.addWidget(self.info_layout)

        self.retranslateUi(DetectorWindow)
        QMetaObject.connectSlotsByName(DetectorWindow)

    def retranslateUi(self, DetectorWindow):
        _translate = QCoreApplication.translate
        DetectorWindow.setWindowTitle(_translate("CollimatorWindow", "Collimator Settings"))
        self.xcoord_label.setText(_translate("CollimatorWindow", "X:"))
        self.xcoord_box.setSuffix(_translate("CollimatorWindow", " mm"))
        self.ycoord_label.setText(_translate("CollimatorWindow", "Y:"))
        self.ycoord_box.setSuffix(_translate("CollimatorWindow", " mm"))
        self.zcoord_label.setText(_translate("CollimatorWindow", "Z:"))
        self.zcoord_box.setSuffix(_translate("CollimatorWindow", " mm"))
        self.collimator_label.setText(_translate("CollimatorWindow", "Collimator"))
        self.properties_label.setText(_translate("CollimatorWindow", "Radius           &         Thickness"))
        self.radius_label.setText(_translate("CollimatorWindow", "R:"))
        self.radius_box.setSuffix(_translate("CollimatorWindow", " mm"))
        self.thickness_label.setText(_translate("CollimatorWindow", "T:"))
        self.thickness_box.setSuffix(_translate("CollimatorWindow", " mm"))


class CollimatorWindow(QDialog, Ui_CollimatorWindow):
    def __init__(self, collimator: Collimator) -> None:
        # window initializing
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./icon.ico'))

        # collimator
        self.collimator = collimator
        self.set_values()

        # event handling
        ok, cancel = self.okbutton.buttons()
        ok.clicked.connect(self.save)
        cancel.clicked.connect(self.close)

    def set_values(self) -> None:
        self.xcoord_box.setValue(self.collimator.x_position)
        self.ycoord_box.setValue(self.collimator.y_position)
        self.zcoord_box.setValue(self.collimator.z_position)

        self.radius_box.setValue(self.collimator.radius)
        self.thickness_box.setValue(self.collimator.thickness)

    def save(self) -> None:
        xcoord = self.xcoord_box.value()
        ycoord = self.ycoord_box.value()
        zcoord = self.zcoord_box.value()
        radius = self.radius_box.value()
        thickness = self.thickness_box.value()

        dx = xcoord - self.collimator.x_position
        dy = ycoord - self.collimator.y_position
        dz = zcoord - self.collimator.z_position

        self.collimator.move(dx, dy, dz)
        self.collimator.radius = radius
        self.collimator.thickness = thickness

        self.close()


if __name__ == "__main__":
    pass
