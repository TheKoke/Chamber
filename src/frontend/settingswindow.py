from backend.environment import Chamber

from frontend.telescopewindow import TelescopeWindow
from frontend.collimatorwindow import CollimatorWindow

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, 
    QLabel, QSpacerItem, QSizePolicy, 
    QDialogButtonBox, QDialog, QPushButton
)


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(600, 300)
        SettingsWindow.setMinimumSize(QSize(600, 300))
        SettingsWindow.setMaximumSize(QSize(800, 450))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        SettingsWindow.setFont(font)
        self.horizontalLayout = QHBoxLayout(SettingsWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.info_layout = QFrame(SettingsWindow)
        self.info_layout.setFrameShape(QFrame.StyledPanel)
        self.info_layout.setFrameShadow(QFrame.Raised)
        self.info_layout.setObjectName("info_layout")
        self.verticalLayout = QVBoxLayout(self.info_layout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.info_label = QLabel(self.info_layout)
        self.info_label.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        font.setPointSize(20)
        self.info_label.setFont(font)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setObjectName("info_label")
        self.verticalLayout.addWidget(self.info_label)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
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
        self.verticalLayout.addLayout(self.collimators_layout)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.telescopes_layout = QHBoxLayout()
        self.telescopes_layout.setObjectName("telescopes_layout")
        self.telescope1_button = QPushButton(self.info_layout)
        self.telescope1_button.setMinimumSize(QSize(0, 50))
        self.telescope1_button.setObjectName("telescope1_button")
        self.telescopes_layout.addWidget(self.telescope1_button)
        self.telescope2_button = QPushButton(self.info_layout)
        self.telescope2_button.setMinimumSize(QSize(0, 50))
        self.telescope2_button.setObjectName("telescope2_button")
        self.telescopes_layout.addWidget(self.telescope2_button)
        self.telescope3_button = QPushButton(self.info_layout)
        self.telescope3_button.setMinimumSize(QSize(0, 50))
        self.telescope3_button.setObjectName("telescope3_button")
        self.telescopes_layout.addWidget(self.telescope3_button)
        self.verticalLayout.addLayout(self.telescopes_layout)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.okbutton = QDialogButtonBox(self.info_layout)
        self.okbutton.setMaximumSize(QSize(16777215, 50))
        self.okbutton.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.okbutton.setObjectName("okbutton")
        self.verticalLayout.addWidget(self.okbutton)
        self.horizontalLayout.addWidget(self.info_layout)

        self.retranslateUi(SettingsWindow)
        QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Chamber Settings"))
        self.info_label.setText(_translate("SettingsWindow", "Scattering Chamber"))
        self.first_button.setText(_translate("SettingsWindow", "1st collimator"))
        self.second_button.setText(_translate("SettingsWindow", "2nd collimator"))
        self.telescope1_button.setText(_translate("SettingsWindow", "1st telescope"))
        self.telescope2_button.setText(_translate("SettingsWindow", "2nd telescope"))
        self.telescope3_button.setText(_translate("SettingsWindow", "3rd telescope"))


class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self, chamber: Chamber) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        self.chamber = chamber

        self.first_button.clicked.connect(self.open_first_collimator)
        self.second_button.clicked.connect(self.open_second_collimator)
        self.telescope1_button.clicked.connect(self.open_first_telescope)
        self.telescope2_button.clicked.connect(self.open_second_telescope)
        self.telescope3_button.clicked.connect(self.open_third_telescope)

    def open_first_collimator(self) -> None:
        pass

    def open_second_collimator(self) -> None:
        pass

    def open_first_telescope(self) -> None:
        pass

    def open_second_telescope(self) -> None:
        pass

    def open_third_telescope(self) -> None:
        pass


if __name__ == "__main__":
    pass
