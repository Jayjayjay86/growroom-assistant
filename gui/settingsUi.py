import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from logic.jsonFileManager import JSONFileManager
from logic.roomControl import RoomController
from gui.editDialogUi import EditDialogUi
from gui.deleteDialogUi import DeleteDialogUi


class SettingsWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Dialog")
        self.setWindowTitle("Settings")
        self.resize(606, 499)
        self.setStyleSheet(
            "QMenuBar {\n"
            "    background-color: rgb(244, 244, 244);\n"
            "    color: rgb(62, 62, 62);\n"
            "    font-weight: bold;\n"
            "}\n"
            ""
        )
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.dehumidifierFrame = QFrame(self)
        self.dehumidifierFrame.setMinimumSize(QSize(0, 0))
        self.dehumidifierFrame.setStyleSheet("font-size:11px;")
        self.dehumidifierFrame.setFrameShape(QFrame.StyledPanel)
        self.dehumidifierFrame.setFrameShadow(QFrame.Raised)
        self.dehumidifierFrame.setObjectName("dehumidifierFrame")
        self.verticalLayout = QVBoxLayout(self.dehumidifierFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dehumidifier_title_label = QLabel(self.dehumidifierFrame)
        self.dehumidifier_title_label.setStyleSheet("")
        self.dehumidifier_title_label.setObjectName("dehumidifier_title_label")
        self.verticalLayout.addWidget(self.dehumidifier_title_label)
        self.dehumidifier_HLine = QFrame(self.dehumidifierFrame)
        self.dehumidifier_HLine.setFrameShape(QFrame.HLine)
        self.dehumidifier_HLine.setFrameShadow(QFrame.Sunken)
        self.dehumidifier_HLine.setObjectName("dehumidifier_HLine")
        self.verticalLayout.addWidget(self.dehumidifier_HLine)
        self.dehumidifier_listview = QListView(self.dehumidifierFrame)
        self.dehumidifier_listview.setStyleSheet(
            "border-radius:15px;\n"
            "background-color: rgb(255, 255, 247);\n"
            "border: .5px solid rgb(190, 190, 190);"
        )
        self.dehumidifier_listview.setObjectName("dehumidifier_listview")
        self.verticalLayout.addWidget(self.dehumidifier_listview)
        self.dehumidifier_delete_pushbutton = QPushButton(self.dehumidifierFrame)
        self.dehumidifier_delete_pushbutton.setObjectName(
            "dehumidifier_delete_pushbutton"
        )
        self.verticalLayout.addWidget(self.dehumidifier_delete_pushbutton)
        self.dehumidifier_edit_pushbutton = QPushButton(self.dehumidifierFrame)
        self.dehumidifier_edit_pushbutton.setObjectName("dehumidifier_edit_pushbutton")
        self.verticalLayout.addWidget(self.dehumidifier_edit_pushbutton)
        self.gridLayout.addWidget(self.dehumidifierFrame, 2, 0, 1, 1)
        self.title_label = QLabel(self)
        self.title_label.setObjectName("title_label")
        self.gridLayout.addWidget(self.title_label, 0, 0, 1, 1)
        self.addNewFrame = QFrame(self)
        self.addNewFrame.setStyleSheet("font-size:11px;")
        self.addNewFrame.setFrameShape(QFrame.StyledPanel)
        self.addNewFrame.setFrameShadow(QFrame.Raised)
        self.addNewFrame.setObjectName("addNewFrame")
        self.verticalLayout_2 = QVBoxLayout(self.addNewFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.add_title_label = QLabel(self.addNewFrame)
        self.add_title_label.setStyleSheet("")
        self.add_title_label.setObjectName("add_title_label")
        self.verticalLayout_2.addWidget(self.add_title_label)
        self.dehumidifier_HLine_2 = QFrame(self.addNewFrame)
        self.dehumidifier_HLine_2.setFrameShape(QFrame.HLine)
        self.dehumidifier_HLine_2.setFrameShadow(QFrame.Sunken)
        self.dehumidifier_HLine_2.setObjectName("dehumidifier_HLine_2")
        self.verticalLayout_2.addWidget(self.dehumidifier_HLine_2)
        self.ipLayout = QHBoxLayout()
        self.ipLayout.setObjectName("ipLayout")
        self.ip_label = QLabel(self.addNewFrame)
        self.ip_label.setMinimumSize(QSize(40, 0))
        self.ip_label.setStyleSheet("")
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
        self.addHLine = QFrame(self.addNewFrame)
        self.addHLine.setFrameShape(QFrame.HLine)
        self.addHLine.setFrameShadow(QFrame.Sunken)
        self.addHLine.setObjectName("addHLine")
        self.verticalLayout_2.addWidget(self.addHLine)
        self.tokenLayout = QHBoxLayout()
        self.tokenLayout.setObjectName("tokenLayout")
        self.token_label = QLabel(self.addNewFrame)
        self.token_label.setMinimumSize(QSize(40, 0))
        self.token_label.setStyleSheet("")
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
        self.addButtonLayout = QHBoxLayout()
        self.addButtonLayout.setObjectName("addButtonLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.addButtonLayout.addItem(spacerItem)
        self.addPushButton = QPushButton(self.addNewFrame)
        self.addPushButton.setObjectName("addPushButton")
        self.addButtonLayout.addWidget(self.addPushButton)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.addButtonLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.addButtonLayout)
        self.gridLayout.addWidget(self.addNewFrame, 3, 0, 1, 1)
        self.thresholdsFrame = QFrame(self)
        self.thresholdsFrame.setStyleSheet("font-size:11px;")
        self.thresholdsFrame.setFrameShape(QFrame.StyledPanel)
        self.thresholdsFrame.setFrameShadow(QFrame.Raised)
        self.thresholdsFrame.setObjectName("thresholdsFrame")
        self.verticalLayout_5 = QVBoxLayout(self.thresholdsFrame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.thresholds_title_label = QLabel(self.thresholdsFrame)
        self.thresholds_title_label.setStyleSheet("")
        self.thresholds_title_label.setObjectName("thresholds_title_label")
        self.verticalLayout_5.addWidget(self.thresholds_title_label)
        self.dehumidifier_HLine_5 = QFrame(self.thresholdsFrame)
        self.dehumidifier_HLine_5.setFrameShape(QFrame.HLine)
        self.dehumidifier_HLine_5.setFrameShadow(QFrame.Sunken)
        self.dehumidifier_HLine_5.setObjectName("dehumidifier_HLine_5")
        self.verticalLayout_5.addWidget(self.dehumidifier_HLine_5)
        self.humidity_thresh_title_label = QLabel(self.thresholdsFrame)
        self.humidity_thresh_title_label.setStyleSheet("")
        self.humidity_thresh_title_label.setObjectName("humidity_thresh_title_label")
        self.verticalLayout_5.addWidget(self.humidity_thresh_title_label)
        self.vegetationLayout = QHBoxLayout()
        self.vegetationLayout.setObjectName("vegetationLayout")
        self.veg_title_label = QLabel(self.thresholdsFrame)
        self.veg_title_label.setMinimumSize(QSize(40, 0))
        self.veg_title_label.setStyleSheet("")
        self.veg_title_label.setObjectName("veg_title_label")
        self.vegetationLayout.addWidget(self.veg_title_label)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.vegetationLayout.addItem(spacerItem2)
        self.veg_high_label = QLabel(self.thresholdsFrame)
        self.veg_high_label.setObjectName("veg_high_label")
        self.vegetationLayout.addWidget(self.veg_high_label)
        self.veg_high_value = QSpinBox(self.thresholdsFrame)
        self.veg_high_value.setObjectName("veg_high_value")
        self.vegetationLayout.addWidget(self.veg_high_value)
        self.veg_low_label = QLabel(self.thresholdsFrame)
        self.veg_low_label.setObjectName("veg_low_label")
        self.vegetationLayout.addWidget(self.veg_low_label)
        self.veg_low_value = QSpinBox(self.thresholdsFrame)
        self.veg_low_value.setObjectName("veg_low_value")
        self.vegetationLayout.addWidget(self.veg_low_value)
        self.verticalLayout_5.addLayout(self.vegetationLayout)
        self.floweringLayout = QHBoxLayout()
        self.floweringLayout.setObjectName("floweringLayout")
        self.flowering_title_label = QLabel(self.thresholdsFrame)
        self.flowering_title_label.setMinimumSize(QSize(40, 0))
        self.flowering_title_label.setStyleSheet("")
        self.flowering_title_label.setObjectName("flowering_title_label")
        self.floweringLayout.addWidget(self.flowering_title_label)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.floweringLayout.addItem(spacerItem3)
        self.flowering_high_label = QLabel(self.thresholdsFrame)
        self.flowering_high_label.setObjectName("flowering_high_label")
        self.floweringLayout.addWidget(self.flowering_high_label)
        self.flowering_high_value = QSpinBox(self.thresholdsFrame)
        self.flowering_high_value.setObjectName("flowering_high_value")
        self.floweringLayout.addWidget(self.flowering_high_value)
        self.flowering_low_label = QLabel(self.thresholdsFrame)
        self.flowering_low_label.setObjectName("flowering_low_label")
        self.floweringLayout.addWidget(self.flowering_low_label)
        self.flowering_low_value = QSpinBox(self.thresholdsFrame)
        self.flowering_low_value.setObjectName("flowering_low_value")
        self.floweringLayout.addWidget(self.flowering_low_value)
        self.verticalLayout_5.addLayout(self.floweringLayout)
        self.curingLayout = QHBoxLayout()
        self.curingLayout.setObjectName("curingLayout")
        self.curing_title_label = QLabel(self.thresholdsFrame)
        self.curing_title_label.setMinimumSize(QSize(40, 0))
        self.curing_title_label.setStyleSheet("")
        self.curing_title_label.setObjectName("curing_title_label")
        self.curingLayout.addWidget(self.curing_title_label)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.curingLayout.addItem(spacerItem4)
        self.curing_high_label = QLabel(self.thresholdsFrame)
        self.curing_high_label.setObjectName("curing_high_label")
        self.curingLayout.addWidget(self.curing_high_label)
        self.curing_high_value = QSpinBox(self.thresholdsFrame)
        self.curing_high_value.setObjectName("curing_high_value")
        self.curingLayout.addWidget(self.curing_high_value)
        self.curing_low_label = QLabel(self.thresholdsFrame)
        self.curing_low_label.setObjectName("curing_low_label")
        self.curingLayout.addWidget(self.curing_low_label)
        self.curing_low_value = QSpinBox(self.thresholdsFrame)
        self.curing_low_value.setObjectName("curing_low_value")
        self.curingLayout.addWidget(self.curing_low_value)
        self.verticalLayout_5.addLayout(self.curingLayout)
        self.lightsHLine_2 = QFrame(self.thresholdsFrame)
        self.lightsHLine_2.setFrameShape(QFrame.HLine)
        self.lightsHLine_2.setFrameShadow(QFrame.Sunken)
        self.lightsHLine_2.setObjectName("lightsHLine_2")
        self.verticalLayout_5.addWidget(self.lightsHLine_2)
        self.warningLayout = QHBoxLayout()
        self.warningLayout.setObjectName("warningLayout")
        self.warning_title_label = QLabel(self.thresholdsFrame)
        self.warning_title_label.setMinimumSize(QSize(40, 0))
        self.warning_title_label.setStyleSheet("")
        self.warning_title_label.setObjectName("warning_title_label")
        self.warningLayout.addWidget(self.warning_title_label)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.warningLayout.addItem(spacerItem5)
        self.warning_high_label = QLabel(self.thresholdsFrame)
        self.warning_high_label.setObjectName("warning_high_label")
        self.warningLayout.addWidget(self.warning_high_label)
        self.warning_high_value = QSpinBox(self.thresholdsFrame)
        self.warning_high_value.setObjectName("warning_high_value")
        self.warningLayout.addWidget(self.warning_high_value)
        self.warning_low_label = QLabel(self.thresholdsFrame)
        self.warning_low_label.setObjectName("warning_low_label")
        self.warningLayout.addWidget(self.warning_low_label)
        self.warning_low_value = QSpinBox(self.thresholdsFrame)
        self.warning_low_value.setObjectName("warning_low_value")
        self.warningLayout.addWidget(self.warning_low_value)
        self.verticalLayout_5.addLayout(self.warningLayout)
        self.dehumidifier_HLine_8 = QFrame(self.thresholdsFrame)
        self.dehumidifier_HLine_8.setFrameShape(QFrame.HLine)
        self.dehumidifier_HLine_8.setFrameShadow(QFrame.Sunken)
        self.dehumidifier_HLine_8.setObjectName("dehumidifier_HLine_8")
        self.verticalLayout_5.addWidget(self.dehumidifier_HLine_8)
        self.temp_thresholds_title_label = QLabel(self.thresholdsFrame)
        self.temp_thresholds_title_label.setStyleSheet("")
        self.temp_thresholds_title_label.setObjectName("temp_thresholds_title_label")
        self.verticalLayout_5.addWidget(self.temp_thresholds_title_label)
        self.dayTempLayout = QHBoxLayout()
        self.dayTempLayout.setObjectName("dayTempLayout")
        self.day_title_label = QLabel(self.thresholdsFrame)
        self.day_title_label.setMinimumSize(QSize(40, 0))
        self.day_title_label.setStyleSheet("")
        self.day_title_label.setObjectName("day_title_label")
        self.dayTempLayout.addWidget(self.day_title_label)
        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.dayTempLayout.addItem(spacerItem6)
        self.day_high_label = QLabel(self.thresholdsFrame)
        self.day_high_label.setObjectName("day_high_label")
        self.dayTempLayout.addWidget(self.day_high_label)
        self.day_high_value = QSpinBox(self.thresholdsFrame)
        self.day_high_value.setObjectName("day_high_value")
        self.dayTempLayout.addWidget(self.day_high_value)
        self.day_low_label = QLabel(self.thresholdsFrame)
        self.day_low_label.setObjectName("day_low_label")
        self.dayTempLayout.addWidget(self.day_low_label)
        self.day_low_value = QSpinBox(self.thresholdsFrame)
        self.day_low_value.setObjectName("day_low_value")
        self.dayTempLayout.addWidget(self.day_low_value)
        self.verticalLayout_5.addLayout(self.dayTempLayout)
        self.nightTempLayout = QHBoxLayout()
        self.nightTempLayout.setObjectName("nightTempLayout")
        self.night_title_label = QLabel(self.thresholdsFrame)
        self.night_title_label.setMinimumSize(QSize(40, 0))
        self.night_title_label.setStyleSheet("")
        self.night_title_label.setObjectName("night_title_label")
        self.nightTempLayout.addWidget(self.night_title_label)
        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.nightTempLayout.addItem(spacerItem7)
        self.night_low_label = QLabel(self.thresholdsFrame)
        self.night_low_label.setObjectName("night_low_label")
        self.nightTempLayout.addWidget(self.night_low_label)
        self.night_low_value = QSpinBox(self.thresholdsFrame)
        self.night_low_value.setObjectName("night_low_value")
        self.nightTempLayout.addWidget(self.night_low_value)
        self.night_high_label = QLabel(self.thresholdsFrame)
        self.night_high_label.setObjectName("night_high_label")
        self.nightTempLayout.addWidget(self.night_high_label)
        self.night_high_value = QSpinBox(self.thresholdsFrame)
        self.night_high_value.setObjectName("night_high_value")
        self.nightTempLayout.addWidget(self.night_high_value)
        self.verticalLayout_5.addLayout(self.nightTempLayout)
        self.gridLayout.addWidget(self.thresholdsFrame, 2, 1, 1, 1)
        self.lightsFrame = QFrame(self)
        self.lightsFrame.setStyleSheet("font-size:11px;")
        self.lightsFrame.setFrameShape(QFrame.StyledPanel)
        self.lightsFrame.setFrameShadow(QFrame.Raised)
        self.lightsFrame.setObjectName("lightsFrame")
        self.verticalLayout_4 = QVBoxLayout(self.lightsFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lights_title_label = QLabel(self.lightsFrame)
        self.lights_title_label.setStyleSheet("")
        self.lights_title_label.setObjectName("lights_title_label")
        self.verticalLayout_4.addWidget(self.lights_title_label)
        self.dehumidifier_HLine_6 = QFrame(self.lightsFrame)
        self.dehumidifier_HLine_6.setFrameShape(QFrame.HLine)
        self.dehumidifier_HLine_6.setFrameShadow(QFrame.Sunken)
        self.dehumidifier_HLine_6.setObjectName("dehumidifier_HLine_6")
        self.verticalLayout_4.addWidget(self.dehumidifier_HLine_6)
        self.lightsOnLayout = QHBoxLayout()
        self.lightsOnLayout.setObjectName("lightsOnLayout")
        self.lights_on_label = QLabel(self.lightsFrame)
        self.lights_on_label.setMinimumSize(QSize(40, 0))
        self.lights_on_label.setStyleSheet("")
        self.lights_on_label.setObjectName("lights_on_label")
        self.lightsOnLayout.addWidget(self.lights_on_label)
        self.lightsOnTimeEdit = QTimeEdit(self.lightsFrame)
        self.lightsOnTimeEdit.setStyleSheet(
            "border-radius:15px;\n"
            "background-color: rgb(255, 255, 247);\n"
            "border: .5px solid rgb(190, 190, 190);"
        )
        self.lightsOnTimeEdit.setObjectName("lightsOnTimeEdit")
        self.lightsOnLayout.addWidget(self.lightsOnTimeEdit)
        self.verticalLayout_4.addLayout(self.lightsOnLayout)
        self.lightsHLine = QFrame(self.lightsFrame)
        self.lightsHLine.setFrameShape(QFrame.HLine)
        self.lightsHLine.setFrameShadow(QFrame.Sunken)
        self.lightsHLine.setObjectName("lightsHLine")
        self.verticalLayout_4.addWidget(self.lightsHLine)
        self.lightsOffLayout = QHBoxLayout()
        self.lightsOffLayout.setObjectName("lightsOffLayout")
        self.lights_off_label = QLabel(self.lightsFrame)
        self.lights_off_label.setMinimumSize(QSize(40, 0))
        self.lights_off_label.setStyleSheet("")
        self.lights_off_label.setObjectName("lights_off_label")
        self.lightsOffLayout.addWidget(self.lights_off_label)
        self.lightsOffTimeEdit = QTimeEdit(self.lightsFrame)
        self.lightsOffTimeEdit.setStyleSheet(
            "border-radius:15px;\n"
            "background-color: rgb(255, 255, 247);\n"
            "border: .5px solid rgb(190, 190, 190);"
        )
        self.lightsOffTimeEdit.setObjectName("lightsOffTimeEdit")
        self.lightsOffLayout.addWidget(self.lightsOffTimeEdit)
        self.verticalLayout_4.addLayout(self.lightsOffLayout)
        self.gridLayout.addWidget(self.lightsFrame, 3, 1, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStyleSheet("font-size:13px;")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Save
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        # Initialize the listview model
        self.model = QStandardItemModel()
        self.dehumidifier_listview.setModel(self.model)
        # function calls
        self.populateListView()
        self.populateSettings()

        # Triggers
        self.addPushButton.clicked.connect(self.add_new_dehumidifier)
        self.dehumidifier_edit_pushbutton.clicked.connect(self.handleClickEdit)
        self.dehumidifier_delete_pushbutton.clicked.connect(self.handleClickDelete)

        self.buttonBox.accepted.connect(self.handleAccept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore

        QMetaObject.connectSlotsByName(self)

        self.dehumidifier_title_label.setText("Dehumidifiers:")
        self.dehumidifier_delete_pushbutton.setText("Delete")
        self.dehumidifier_edit_pushbutton.setText("Edit")
        self.title_label.setText("Settings:")
        self.add_title_label.setText("Add New Dehumidifier Unit:")
        self.ip_label.setText("Ip:")
        self.token_label.setText("token:")
        self.addPushButton.setText("Add")
        self.thresholds_title_label.setText("Thresholds")
        self.humidity_thresh_title_label.setText("Humidty:")
        self.veg_title_label.setText("Vegetation:")
        self.veg_high_label.setText("high")
        self.veg_low_label.setText("low")
        self.flowering_title_label.setText("Flowering:")
        self.flowering_high_label.setText("high")
        self.flowering_low_label.setText("low")
        self.curing_title_label.setText("Curing:")
        self.curing_high_label.setText("high")
        self.curing_low_label.setText("low")
        self.warning_title_label.setText("Warning Levels:")
        self.warning_high_label.setText("high")
        self.warning_low_label.setText("low")
        self.temp_thresholds_title_label.setText("Temperature Thresholds:")

        self.day_title_label.setText("Day")
        self.day_high_label.setText("high")
        self.day_low_label.setText("low")
        self.night_title_label.setText("Night")
        self.night_low_label.setText("low")
        self.night_high_label.setText("high")
        self.lights_title_label.setText("Light Settings:")
        self.lights_on_label.setText("Lights On")
        self.lights_off_label.setText("Lights Off")

    def add_new_dehumidifier(self):
        JSONFileManager(selection="devices").create_file_if_not_exists()
        devices = JSONFileManager(selection="devices").read_json()
        device_id = len(devices) + 1
        form_ip = self.ip_lineEdit.text()
        form_token = self.token_lineEdit.text()
        data = {"id": device_id, "ip": form_ip, "token": form_token}
        new_device = RoomController(ip=form_ip, token=form_token)
        try:
            print(new_device.device.info())
            data["active"] = True
            JSONFileManager(selection="devices").add_to_json(data)
            self.show_warning_box(title="Success!", warning="Device Added Successfully")
            self.populateListView()
        except:
            data["active"] = False
            JSONFileManager(selection="devices").add_to_json(data)
            self.show_warning_box(title="Error!", warning="Device Not Found!")
            self.populateListView()
            return

    def handleAccept(self):
        veg_high = self.veg_high_value.value()
        veg_low = self.veg_low_value.value()
        flowering_high = self.flowering_high_value.value()
        flowering_low = self.flowering_low_value.value()
        curing_high = self.curing_high_value.value()
        curing_low = self.curing_low_value.value()
        warning_high = self.warning_high_value.value()
        warning_low = self.warning_low_value.value()
        day_high = self.day_high_value.value()
        day_low = self.day_low_value.value()
        night_high = self.night_high_value.value()
        night_low = self.night_low_value.value()

        onTime = self.lightsOnTimeEdit.time()
        on_hour = onTime.hour()
        on_minute = onTime.minute()
        offTime = self.lightsOffTimeEdit.time()
        off_hour = offTime.hour()
        off_minute = offTime.minute()

        updated_settings = {
            "humidity_thresholds": {
                "vegetative": {"high": veg_high, "low": veg_low},
                "flowering": {"high": flowering_high, "low": flowering_low},
                "curing": {"high": curing_high, "low": curing_low},
            },
            "warning_thresholds": {
                "humidity": {"high": warning_high, "low": warning_low}
            },
            "temperature_thresholds": {
                "day": {"high": day_high, "low": day_low},
                "night": {"high": night_high, "low": night_low},
            },
            "lights": {
                "on": {"hour": on_hour, "minute": on_minute},
                "off": {"hour": off_hour, "minute": off_minute},
            },
        }
        try:
            JSONFileManager(selection="settings").update_settings(updated_settings)
            self.show_warning_box(title="Saved!", warning="Details Saved to disk")
        except:
            self.show_warning_box(title="Error!", warning="Something went wrong :(")
        self.accept()

    def populateSettings(self):
        settings = JSONFileManager(selection="settings").read_json()
        # unpack values
        humidity_thresholds = settings["humidity_thresholds"]
        veg_thresholds = humidity_thresholds["vegetative"]
        veg_high = veg_thresholds["high"]
        veg_low = veg_thresholds["low"]

        flower_thresholds = humidity_thresholds["flowering"]
        flower_high = flower_thresholds["high"]
        flower_low = flower_thresholds["low"]
        cure_thresholds = humidity_thresholds["curing"]
        cure_high = cure_thresholds["high"]
        cure_low = cure_thresholds["low"]

        warning_thresholds = settings["warning_thresholds"]
        warning_humidity = warning_thresholds["humidity"]
        warning_high = warning_humidity["high"]
        warning_low = warning_humidity["low"]

        temp_thresholds = settings["temperature_thresholds"]
        day_temps = temp_thresholds["day"]
        day_high = day_temps["high"]
        day_low = day_temps["low"]

        night_temps = temp_thresholds["night"]
        night_high = night_temps["high"]
        night_low = night_temps["low"]

        lights = settings["lights"]
        lights_on = lights["on"]
        on_hour = lights_on["hour"]
        on_minute = lights_on["minute"]
        lights_off = lights["off"]
        off_hour = lights_off["hour"]
        off_minute = lights_off["minute"]
        # assign values
        self.veg_high_value.setValue(int(veg_high))
        self.veg_low_value.setValue(int(veg_low))
        self.flowering_high_value.setValue(int(flower_high))
        self.flowering_low_value.setValue(int(flower_low))
        self.curing_high_value.setValue(int(cure_high))
        self.curing_low_value.setValue(int(cure_low))
        self.warning_high_value.setValue(int(warning_high))
        self.warning_low_value.setValue(int(warning_low))
        self.day_high_value.setValue(int(day_high))
        self.day_low_value.setValue(int(day_low))
        self.night_high_value.setValue(int(night_high))
        self.night_low_value.setValue(int(night_low))
        on_time = QTime(on_hour, on_minute)
        off_time = QTime(off_hour, off_minute)
        self.lightsOnTimeEdit.setTime(on_time)
        self.lightsOffTimeEdit.setTime(off_time)

    def handleClickEdit(self):
        selected_index = self.dehumidifier_listview.currentIndex()
        if selected_index.isValid():
            device_id = self.model.data(selected_index, Qt.DisplayRole)
            window = EditDialogUi(device_id=int(device_id[4:5]))
            result = window.exec_()
            if result == QDialog.Accepted:
                self.model.clear()
                self.populateListView()
            else:
                return

    def handleClickDelete(self):
        selected_index = self.dehumidifier_listview.currentIndex()
        if selected_index.isValid():
            device_id = self.model.data(selected_index, Qt.DisplayRole)
            window = DeleteDialogUiDialogUi(int(device_id=device_id[4:5]))
            window.exec_()
        else:
            return

        return

    def populateListView(self):
        self.model.clear()
        dehumidifier_unit_list = JSONFileManager(selection="devices").read_json()

        for unit in dehumidifier_unit_list:
            active = unit["active"]
            if active == True:
                active = "Active"
            else:
                active = "Inactive"
            item_text = f"Id: {unit['id']} - Ip: {unit['ip']} - Status: {active}"
            item = QStandardItem(item_text)
            self.model.appendRow(item)

    def show_warning_box(self, title, warning):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(warning)
        msg_box.exec_()


settingsApp = QApplication(sys.argv)
settingsUi = SettingsWindow()
