from backend.environment import Target

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, 
    QLabel, QDoubleSpinBox, QSpacerItem, 
    QSizePolicy, QDialogButtonBox, QDialog, QWidget
)


class Ui_TargetWindow(object):
    def setupUi(self, DetectorWindow):
        DetectorWindow.setObjectName("TargetWindow")
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
        self.target_label = QLabel(self.info_layout)
        self.target_label.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        font.setPointSize(20)
        self.target_label.setFont(font)
        self.target_label.setAlignment(Qt.AlignCenter)
        self.target_label.setObjectName("target_label")
        self.verticalLayout_2.addWidget(self.target_label)
        self.properties_label = QLabel(self.info_layout)
        self.properties_label.setAlignment(Qt.AlignCenter)
        self.properties_label.setObjectName("properties_label")
        self.verticalLayout_2.addWidget(self.properties_label)
        self.properties_layout = QHBoxLayout()
        self.properties_layout.setObjectName("properties_layout")
        self.width_layout = QHBoxLayout()
        self.width_layout.setObjectName("width_layout")
        self.width_label = QLabel(self.info_layout)
        self.width_label.setMaximumSize(QSize(16777215, 40))
        self.width_label.setAlignment(Qt.AlignCenter)
        self.width_label.setObjectName("width_label")
        self.width_layout.addWidget(self.width_label)
        self.width_box = QDoubleSpinBox(self.info_layout)
        self.width_box.setMaximum(999999999.0)
        self.width_box.setSingleStep(0.1)
        self.width_box.setProperty("value", 10.0)
        self.width_box.setObjectName("width_box")
        self.width_layout.addWidget(self.width_box)
        self.properties_layout.addLayout(self.width_layout)
        self.height_layout = QHBoxLayout()
        self.height_layout.setObjectName("height_layout")
        self.height_label = QLabel(self.info_layout)
        self.height_label.setMaximumSize(QSize(16777215, 40))
        self.height_label.setAlignment(Qt.AlignCenter)
        self.height_label.setObjectName("height_label")
        self.height_layout.addWidget(self.height_label)
        self.height_box = QDoubleSpinBox(self.info_layout)
        self.height_box.setMaximum(999999999.0)
        self.height_box.setSingleStep(0.1)
        self.height_box.setProperty("value", 10.0)
        self.height_box.setObjectName("height_box")
        self.height_layout.addWidget(self.height_box)
        self.properties_layout.addLayout(self.height_layout)
        self.verticalLayout_2.addLayout(self.properties_layout)
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
        DetectorWindow.setWindowTitle(_translate("TargetWindow", "Target Settings - Chamber"))
        self.xcoord_label.setText(_translate("TargetWindow", "X:"))
        self.xcoord_box.setSuffix(_translate("TargetWindow", " mm"))
        self.ycoord_label.setText(_translate("TargetWindow", "Y:"))
        self.ycoord_box.setSuffix(_translate("TargetWindow", " mm"))
        self.zcoord_label.setText(_translate("TargetWindow", "Z:"))
        self.zcoord_box.setSuffix(_translate("TargetWindow", " mm"))
        self.target_label.setText(_translate("TargetWindow", "Thick Target"))
        self.properties_label.setText(_translate("TargetWindow", "Width           &         Height"))
        self.width_label.setText(_translate("TargetWindow", "W:"))
        self.width_box.setSuffix(_translate("TargetWindow", " mm"))
        self.height_label.setText(_translate("TargetWindow", "H:"))
        self.height_box.setSuffix(_translate("TargetWindow", " mm"))


class TargetWindow(QDialog, Ui_TargetWindow):
    def __init__(self, target: Target) -> None:
        # window initializing
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./icon.ico'))

        # target
        self.target = target
        self.set_values()

        # event handling
        ok, cancel = self.okbutton.buttons()
        ok.clicked.connect(self.save)
        cancel.clicked.connect(self.close)

    def set_values(self) -> None:
        self.xcoord_box.setValue(self.target.x_position)
        self.ycoord_box.setValue(self.target.y_position)
        self.zcoord_box.setValue(self.target.z_position)

        self.width_box.setValue(self.target.width)
        self.height_box.setValue(self.target.height)

    def save(self) -> None:
        xcoord = self.xcoord_box.value()
        ycoord = self.ycoord_box.value()
        zcoord = self.zcoord_box.value()
        width = self.width_box.value()
        height = self.height_box.value()

        dx = xcoord - self.target.x_position
        dy = ycoord - self.target.y_position
        dz = zcoord - self.target.z_position

        self.target.move(dx, dy, dz)
        self.target.width = width
        self.target.height = height

        self.close()


if __name__ == "__main__":
    pass
