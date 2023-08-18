import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from logic.jsonFileManager import JSONFileManager
from logic.roomControl import RoomController


class EditDialogUi(QDialog):
    def __init__(self, device_id) -> None:
        super().__init__()
        self.device_id = device_id
        self.setObjectName("Dialog")
        self.setWindowTitle("Edit")
        self.resize(456, 174)
        self.setStyleSheet(
            "QMenuBar {\n"
            "    background-color: rgb(244, 244, 244);\n"
            "    color: rgb(62, 62, 62);\n"
            "    font-weight: bold;\n"
            "}\n"
            ""
        )
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QLabel(self)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.addNewFrame = QFrame(self)
        self.addNewFrame.setStyleSheet("font-size:11px;")
        self.addNewFrame.setFrameShape(QFrame.StyledPanel)
        self.addNewFrame.setFrameShadow(QFrame.Raised)
        self.addNewFrame.setObjectName("addNewFrame")
        self.verticalLayout_2 = QVBoxLayout(self.addNewFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.idHLayout = QHBoxLayout()
        self.idHLayout.setObjectName("idHLayout")
        self.id_label = QLabel(self.addNewFrame)
        self.id_label.setStyleSheet("")
        self.id_label.setObjectName("id_label")
        self.idHLayout.addWidget(self.id_label)
        self.id_value = QLabel(self.addNewFrame)
        self.id_value.setStyleSheet(
            "border-radius:15px;\n"
            "background-color: rgb(255, 255, 247);\n"
            "border: .5px solid rgb(190, 190, 190);"
        )
        self.id_value.setAlignment(Qt.AlignCenter)
        self.id_value.setObjectName("id_value")
        self.idHLayout.addWidget(self.id_value)
        self.verticalLayout_2.addLayout(self.idHLayout)
        self.ipLayout = QHBoxLayout()
        self.ipLayout.setObjectName("ipLayout")
        self.ip_label = QLabel(self.addNewFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ip_label.sizePolicy().hasHeightForWidth())
        self.ip_label.setSizePolicy(sizePolicy)
        self.ip_label.setMinimumSize(QSize(40, 0))
        self.ip_label.setStyleSheet("")
        self.ip_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.ip_label.setObjectName("ip_label")
        self.ipLayout.addWidget(self.ip_label)
        self.ip_lineEdit = QLineEdit(self.addNewFrame)
        self.ip_lineEdit.setStyleSheet(
            "border-radius:15px;\n"
            "background-color: rgb(255, 255, 247);\n"
            "border: .5px solid rgb(190, 190, 190);"
        )
        self.ip_lineEdit.setObjectName("ip_lineEdit")
        self.ipLayout.addWidget(self.ip_lineEdit)
        self.verticalLayout_2.addLayout(self.ipLayout)
        self.tokenLayout = QHBoxLayout()
        self.tokenLayout.setObjectName("tokenLayout")
        self.token_label = QLabel(self.addNewFrame)
        self.token_label.setMinimumSize(QSize(40, 0))
        self.token_label.setStyleSheet("")
        self.token_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.token_label.setObjectName("token_label")
        self.tokenLayout.addWidget(self.token_label)
        self.token_lineEdit = QLineEdit(self.addNewFrame)
        self.token_lineEdit.setStyleSheet(
            "border-radius:15px;\n"
            "background-color: rgb(255, 255, 247);\n"
            "border: .5px solid rgb(190, 190, 190);"
        )
        self.token_lineEdit.setObjectName("token_lineEdit")
        self.tokenLayout.addWidget(self.token_lineEdit)
        self.verticalLayout_2.addLayout(self.tokenLayout)
        self.verticalLayout.addWidget(self.addNewFrame)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStyleSheet("font-size:13px;")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.buttonBox.accepted.connect(self.handlesaveDetails)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QMetaObject.connectSlotsByName(self)

        self.title_label.setText("Edit Dehumidifier:")
        self.id_label.setText("Dehumidifier Id:")
        self.id_value.setText("Id")
        self.ip_label.setText("Ip:")
        self.token_label.setText("token:")

        # initialize values
        self.id = int()
        self.active = bool()
        # function calls
        self.populate_fields()

    def populate_fields(self):
        dehumidifierUnitList = JSONFileManager(selection="devices").read_json()
        for device in dehumidifierUnitList:
            if self.device_id == int(device["id"]):
                self.ip_lineEdit.setText(device["ip"])
                self.token_lineEdit.setText(device["token"])

    def handlesaveDetails(self):
        dehumidifierUnitList = JSONFileManager(selection="devices").read_json()
        new_ip = self.ip_lineEdit.text()
        new_token = self.token_lineEdit.text()

        for unit in dehumidifierUnitList:
            if self.device_id == int(unit["id"]):
                self.id = int(unit["id"])
                self.active = unit["active"]

            try:
                RoomController(ip=new_ip, token=new_token).device.info()
                new_active = True

            except:
                new_active = False
                self.show_warning_box(title="Error!", warning="Unit Not Found")
                return
            new_object = {
                "id": self.id,
                "ip": new_ip,
                "token": new_token,
                "active": new_active,
            }
            if self.active:
                # do something to stop the room search before updating list
                self.show_warning_box(
                    title="Error!", warning="Device currently in use."
                )
            else:
                JSONFileManager(selection="devices").replace_object_by_id(
                    id=self.device_id, new_object=new_object
                )
                self.show_warning_box(title="Completed", warning="Details updated.")
                self.accept()

    def show_warning_box(self, title, warning):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(warning)
        msg_box.exec_()
