from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetectorWindow(object):
    def setupUi(self, DetectorWindow):
        DetectorWindow.setObjectName("DetectorWindow")
        DetectorWindow.resize(600, 300)
        DetectorWindow.setMinimumSize(QtCore.QSize(600, 300))
        DetectorWindow.setMaximumSize(QtCore.QSize(800, 450))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        DetectorWindow.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DetectorWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.coordiantes_layout = QtWidgets.QFrame(DetectorWindow)
        self.coordiantes_layout.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.coordiantes_layout.setFrameShadow(QtWidgets.QFrame.Raised)
        self.coordiantes_layout.setObjectName("coordiantes_layout")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.coordiantes_layout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.xcoord_layout = QtWidgets.QHBoxLayout()
        self.xcoord_layout.setObjectName("xcoord_layout")
        self.xcoord_label = QtWidgets.QLabel(self.coordiantes_layout)
        self.xcoord_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.xcoord_label.setAlignment(QtCore.Qt.AlignCenter)
        self.xcoord_label.setObjectName("xcoord_label")
        self.xcoord_layout.addWidget(self.xcoord_label)
        self.xcoord_box = QtWidgets.QDoubleSpinBox(self.coordiantes_layout)
        self.xcoord_box.setMaximum(999999999.0)
        self.xcoord_box.setSingleStep(0.1)
        self.xcoord_box.setObjectName("xcoord_box")
        self.xcoord_layout.addWidget(self.xcoord_box)
        self.verticalLayout.addLayout(self.xcoord_layout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.ycoord_layout = QtWidgets.QHBoxLayout()
        self.ycoord_layout.setObjectName("ycoord_layout")
        self.ycoord_label = QtWidgets.QLabel(self.coordiantes_layout)
        self.ycoord_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.ycoord_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ycoord_label.setObjectName("ycoord_label")
        self.ycoord_layout.addWidget(self.ycoord_label)
        self.ycoord_box = QtWidgets.QDoubleSpinBox(self.coordiantes_layout)
        self.ycoord_box.setMaximum(999999999.0)
        self.ycoord_box.setSingleStep(0.1)
        self.ycoord_box.setObjectName("ycoord_box")
        self.ycoord_layout.addWidget(self.ycoord_box)
        self.verticalLayout.addLayout(self.ycoord_layout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.zcoord_layout = QtWidgets.QHBoxLayout()
        self.zcoord_layout.setObjectName("zcoord_layout")
        self.zcoord_label = QtWidgets.QLabel(self.coordiantes_layout)
        self.zcoord_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.zcoord_label.setAlignment(QtCore.Qt.AlignCenter)
        self.zcoord_label.setObjectName("zcoord_label")
        self.zcoord_layout.addWidget(self.zcoord_label)
        self.zcoord_box = QtWidgets.QDoubleSpinBox(self.coordiantes_layout)
        self.zcoord_box.setMaximum(999999999.0)
        self.zcoord_box.setSingleStep(0.1)
        self.zcoord_box.setObjectName("zcoord_box")
        self.zcoord_layout.addWidget(self.zcoord_box)
        self.verticalLayout.addLayout(self.zcoord_layout)
        self.horizontalLayout.addWidget(self.coordiantes_layout)
        self.info_layout = QtWidgets.QFrame(DetectorWindow)
        self.info_layout.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.info_layout.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_layout.setObjectName("info_layout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.info_layout)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.collimator_label = QtWidgets.QLabel(self.info_layout)
        self.collimator_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.collimator_label.setFont(font)
        self.collimator_label.setAlignment(QtCore.Qt.AlignCenter)
        self.collimator_label.setObjectName("collimator_label")
        self.verticalLayout_2.addWidget(self.collimator_label)
        self.properties_label = QtWidgets.QLabel(self.info_layout)
        self.properties_label.setAlignment(QtCore.Qt.AlignCenter)
        self.properties_label.setObjectName("properties_label")
        self.verticalLayout_2.addWidget(self.properties_label)
        self.properties_layout = QtWidgets.QHBoxLayout()
        self.properties_layout.setObjectName("properties_layout")
        self.radius_layout = QtWidgets.QHBoxLayout()
        self.radius_layout.setObjectName("radius_layout")
        self.radius_label = QtWidgets.QLabel(self.info_layout)
        self.radius_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.radius_label.setAlignment(QtCore.Qt.AlignCenter)
        self.radius_label.setObjectName("radius_label")
        self.radius_layout.addWidget(self.radius_label)
        self.radius_box = QtWidgets.QDoubleSpinBox(self.info_layout)
        self.radius_box.setMaximum(999999999.0)
        self.radius_box.setSingleStep(0.1)
        self.radius_box.setProperty("value", 3.0)
        self.radius_box.setObjectName("radius_box")
        self.radius_layout.addWidget(self.radius_box)
        self.properties_layout.addLayout(self.radius_layout)
        self.thickness_layout = QtWidgets.QHBoxLayout()
        self.thickness_layout.setObjectName("thickness_layout")
        self.thickness_label = QtWidgets.QLabel(self.info_layout)
        self.thickness_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.thickness_label.setAlignment(QtCore.Qt.AlignCenter)
        self.thickness_label.setObjectName("thickness_label")
        self.thickness_layout.addWidget(self.thickness_label)
        self.thickness_box = QtWidgets.QDoubleSpinBox(self.info_layout)
        self.thickness_box.setMaximum(999999999.0)
        self.thickness_box.setSingleStep(0.1)
        self.thickness_box.setProperty("value", 2.0)
        self.thickness_box.setObjectName("thickness_box")
        self.thickness_layout.addWidget(self.thickness_box)
        self.properties_layout.addLayout(self.thickness_layout)
        self.verticalLayout_2.addLayout(self.properties_layout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.okbutton = QtWidgets.QDialogButtonBox(self.info_layout)
        self.okbutton.setMaximumSize(QtCore.QSize(16777215, 50))
        self.okbutton.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.okbutton.setObjectName("okbutton")
        self.verticalLayout_2.addWidget(self.okbutton)
        self.horizontalLayout.addWidget(self.info_layout)

        self.retranslateUi(DetectorWindow)
        QtCore.QMetaObject.connectSlotsByName(DetectorWindow)

    def retranslateUi(self, DetectorWindow):
        _translate = QtCore.QCoreApplication.translate
        DetectorWindow.setWindowTitle(_translate("DetectorWindow", "Detector Settings"))
        self.xcoord_label.setText(_translate("DetectorWindow", "X:"))
        self.xcoord_box.setSuffix(_translate("DetectorWindow", " mm"))
        self.ycoord_label.setText(_translate("DetectorWindow", "Y:"))
        self.ycoord_box.setSuffix(_translate("DetectorWindow", " mm"))
        self.zcoord_label.setText(_translate("DetectorWindow", "Z:"))
        self.zcoord_box.setSuffix(_translate("DetectorWindow", " mm"))
        self.collimator_label.setText(_translate("DetectorWindow", "Collimator"))
        self.properties_label.setText(_translate("DetectorWindow", "Radius           &         Thickness"))
        self.radius_label.setText(_translate("DetectorWindow", "R:"))
        self.radius_box.setSuffix(_translate("DetectorWindow", " mm"))
        self.thickness_label.setText(_translate("DetectorWindow", "T:"))
        self.thickness_box.setSuffix(_translate("DetectorWindow", " mm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DetectorWindow = QtWidgets.QDialog()
    ui = Ui_DetectorWindow()
    ui.setupUi(DetectorWindow)
    DetectorWindow.show()
    sys.exit(app.exec_())
