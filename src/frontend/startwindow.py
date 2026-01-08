from backend.start import starting_position
from frontend.geomwindow import GeomWindow

from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
    QFrame, QLabel, QPushButton, QSizePolicy, QSpacerItem
)


class Ui_StartWindow(object):
    def setupUi(self, StartWindow):
        StartWindow.setObjectName("StartWindow")
        StartWindow.resize(400, 300)
        StartWindow.setMinimumSize(QSize(400, 300))
        StartWindow.setMaximumSize(QSize(400, 300))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        StartWindow.setFont(font)
        self.horizontalLayout = QHBoxLayout(StartWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_frame = QFrame(StartWindow)
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout = QVBoxLayout(self.main_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logo_layout = QHBoxLayout()
        self.logo_layout.setObjectName("logo_layout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.logo_layout.addItem(spacerItem)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.logo_layout.addItem(spacerItem1)
        self.logo_label = QLabel(self.main_frame)
        self.logo_label.setMaximumSize(QSize(50, 50))
        self.logo_label.setPixmap(QPixmap("./icon.ico"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setObjectName("logo_label")
        self.logo_layout.addWidget(self.logo_label)
        self.verticalLayout.addLayout(self.logo_layout)
        self.info_label = QLabel(self.main_frame)
        font = QFont()
        font.setPointSize(20)
        font.setUnderline(True)
        self.info_label.setFont(font)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setObjectName("info_label")
        self.verticalLayout.addWidget(self.info_label)
        self.full_layout = QHBoxLayout()
        self.full_layout.setObjectName("full_layout")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.full_layout.addItem(spacerItem2)
        self.full_button = QPushButton(self.main_frame)
        self.full_button.setMinimumSize(QSize(185, 50))
        self.full_button.setObjectName("full_button")
        self.full_layout.addWidget(self.full_button)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.full_layout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.full_layout)
        self.unscale_layout = QHBoxLayout()
        self.unscale_layout.setObjectName("unscale_layout")
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.unscale_layout.addItem(spacerItem4)
        self.unscale_button = QPushButton(self.main_frame)
        self.unscale_button.setMinimumSize(QSize(185, 50))
        self.unscale_button.setObjectName("unscale_button")
        self.unscale_layout.addWidget(self.unscale_button)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.unscale_layout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.unscale_layout)
        self.label = QLabel(self.main_frame)
        self.label.setMaximumSize(QSize(16777215, 14))
        font = QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.main_frame)

        self.retranslateUi(StartWindow)
        QMetaObject.connectSlotsByName(StartWindow)

    def retranslateUi(self, StartWindow):
        _translate = QCoreApplication.translate
        StartWindow.setWindowTitle(_translate("StartWindow", "Chamber"))
        self.info_label.setText(_translate("StartWindow", "Please choose the scale"))
        self.full_button.setText(_translate("StartWindow", "Full Scale"))
        self.unscale_button.setText(_translate("StartWindow", "Unscale"))
        self.label.setText(_translate("StartWindow", "Laboratory of low-energy nuclear reactions, 2026"))


class StartWindow(QWidget, Ui_StartWindow):
    def __init__(self) -> None:
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        self.full_button.clicked.connect(self.start_full_scale)
        self.unscale_button.clicked.connect(self.start_unscale)

    def start_full_scale(self) -> None:
        self.geom_window = GeomWindow(starting_position(scaled=True))
        self.geom_window.show()
        self.close()

    def start_unscale(self) -> None:
        self.geom_window = GeomWindow(starting_position(scaled=False))
        self.geom_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    startWindow = StartWindow()
    startWindow.show()
    sys.exit(app.exec_())
