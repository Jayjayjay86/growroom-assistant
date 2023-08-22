import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from logic.jsonFileManager import JSONFileManager


class DeleteDialogUi(QDialog):
    def __init__(self, device_id) -> None:
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(439, 82)
        self.setWindowTitle("Confirm Delete")
        self.setStyleSheet(
            "QMenuBar {\n"
            "    background-color: rgb(244, 244, 244);\n"
            "    color: rgb(62, 62, 62);\n"
            "    font-weight: bold;\n"
            "}\n"
            ""
        )
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.warning_label = QLabel(Dialog)
        self.warning_label.setObjectName("warning_label")
        self.horizontalLayout.addWidget(self.warning_label)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonVerticalLayout = QVBoxLayout()
        self.buttonVerticalLayout.setObjectName("buttonVerticalLayout")
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.buttonVerticalLayout.addItem(spacerItem2)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setStyleSheet("font-size:13px;")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonVerticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.buttonVerticalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.deleteFromDeviceList)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QMetaObject.connectSlotsByName(Dialog)
        self.warning_label.setText(f"Remove device with id - {device_id} From List?")

    def deleteFromDeviceList(self):
        JSONFileManager(selection="devices").delete_by_id(device_id)
        self.accept()
