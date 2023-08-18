import sys
from datetime import datetime
import datetime as dt
from logic.jsonFileManager import JSONFileManager
from logic.roomControl import RoomController
from gui.settingsUi import settingsUi, settingsApp

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


style_lights_on = (
    "border-radius:10px;\n"
    "border:0.5px solid black;\n"
    "background-color: rgb(255, 255, 127);"
)
style_lights_off = (
    "border-radius:10px;\n"
    "border:0.5px solid black;\n"
    "background-color: rgb(0, 16, 0);"
)
style_active_on = (
    "border-radius:10px;\n"
    "border:0.5px solid black;\n"
    "background-color: rgb(152, 255, 147);"
)
style_active_off = (
    "border-radius:10px;\n"
    "border:0.5px solid black;\n"
    "background-color: rgb(0, 16, 0);"
)
degree_symbol = "\u00b0"
REFRESH_VALUES_TIMER_MILLIS = 12000
SEND_ROOM_CONTROL_TIMER_MILLIS = 90000
UNIT_HUMIDITY_TARGETS = {"low": 60, "high": 70}


class TheMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(265, 584)
        self.setWindowTitle(("Gro-Ass"))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet(
            "QMenuBar {\n"
            "    background-color: rgb(244, 244, 244);\n"
            "    color: rgb(62, 62, 62);\n"
            "    font-weight: bold;\n"
            "}\n"
            ""
        )

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dateHorizontalLayout = QHBoxLayout()
        self.dateHorizontalLayout.setObjectName("dateHorizontalLayout")
        self.day_value = QLabel(self.centralwidget)
        self.day_value.setStyleSheet("\n" "font-size: 14px;")
        self.day_value.setAlignment(Qt.AlignCenter)
        self.day_value.setObjectName("day_value")
        self.dateHorizontalLayout.addWidget(self.day_value)
        self.month_value = QLabel(self.centralwidget)
        self.month_value.setStyleSheet("\n" "font-size: 14px;")
        self.month_value.setAlignment(Qt.AlignCenter)
        self.month_value.setObjectName("month_value")
        self.dateHorizontalLayout.addWidget(self.month_value)
        self.time_value = QLabel(self.centralwidget)
        self.time_value.setStyleSheet(
            'font: italic 9pt "Digital-7 Mono";\n' "font-size: 17px;"
        )
        self.time_value.setAlignment(Qt.AlignCenter)
        self.time_value.setObjectName("time_value")
        self.dateHorizontalLayout.addWidget(self.time_value)
        self.verticalLayout_2.addLayout(self.dateHorizontalLayout)
        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.mode_label = QLabel(self.centralwidget)
        self.mode_label.setStyleSheet("font-size:10px;")
        self.mode_label.setObjectName("mode_label")
        self.verticalLayout_2.addWidget(self.mode_label)
        self.mode_combo = QComboBox(self.centralwidget)
        self.mode_combo.setStyleSheet("background-color: rgb(255, 222, 144);")
        self.mode_combo.setObjectName("mode_combo")

        self.verticalLayout_2.addWidget(self.mode_combo)
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.unit_details_label = QLabel(self.centralwidget)
        self.unit_details_label.setStyleSheet("font-size:10px;")
        self.unit_details_label.setObjectName("unit_details_label")
        self.verticalLayout_2.addWidget(self.unit_details_label)
        self.units_combo = QComboBox(self.centralwidget)
        self.units_combo.setStyleSheet("background-color: rgb(255, 222, 144);")
        self.units_combo.setObjectName("units_combo")
        self.units_combo.addItem("")
        self.verticalLayout_2.addWidget(self.units_combo)
        self.humidityFrame = QFrame(self.centralwidget)
        self.humidityFrame.setStyleSheet("")
        self.humidityFrame.setFrameShape(QFrame.StyledPanel)
        self.humidityFrame.setFrameShadow(QFrame.Raised)
        self.humidityFrame.setObjectName("humidityFrame")
        self.horizontalLayout_4 = QHBoxLayout(self.humidityFrame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.humidity_label = QLabel(self.humidityFrame)
        self.humidity_label.setStyleSheet("font-size:15px;")
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.humidity_label.setObjectName("humidity_label")
        self.horizontalLayout_4.addWidget(self.humidity_label)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.humidity_value = QLabel(self.humidityFrame)
        self.humidity_value.setStyleSheet(
            'font: italic 9pt "Digital-7 Mono";\n' "font-size: 23px;"
        )
        self.humidity_value.setAlignment(Qt.AlignCenter)
        self.humidity_value.setObjectName("humidity_value")
        self.horizontalLayout_4.addWidget(self.humidity_value)
        self.verticalLayout_2.addWidget(self.humidityFrame)
        self.temperatrue_frame = QFrame(self.centralwidget)
        self.temperatrue_frame.setStyleSheet("")
        self.temperatrue_frame.setFrameShape(QFrame.StyledPanel)
        self.temperatrue_frame.setFrameShadow(QFrame.Raised)
        self.temperatrue_frame.setObjectName("temperatrue_frame")
        self.horizontalLayout = QHBoxLayout(self.temperatrue_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.temperature_label = QLabel(self.temperatrue_frame)
        self.temperature_label.setStyleSheet("font-size:15px;")
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setObjectName("temperature_label")
        self.horizontalLayout.addWidget(self.temperature_label)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.temperature_value = QLabel(self.temperatrue_frame)
        self.temperature_value.setStyleSheet(
            'font: italic 9pt "Digital-7 Mono";\n' "font-size: 23px;"
        )
        self.temperature_value.setAlignment(Qt.AlignCenter)
        self.temperature_value.setObjectName("temperature_value")
        self.horizontalLayout.addWidget(self.temperature_value)
        self.verticalLayout_2.addWidget(self.temperatrue_frame)
        self.targetFrame = QFrame(self.centralwidget)
        self.targetFrame.setFrameShape(QFrame.StyledPanel)
        self.targetFrame.setFrameShadow(QFrame.Raised)
        self.targetFrame.setObjectName("targetFrame")
        self.horizontalLayout_2 = QHBoxLayout(self.targetFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.target_label = QLabel(self.targetFrame)
        self.target_label.setStyleSheet("font-size:15px;")
        self.target_label.setAlignment(Qt.AlignCenter)
        self.target_label.setObjectName("target_label")
        self.horizontalLayout_2.addWidget(self.target_label)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.target_value = QLabel(self.targetFrame)
        self.target_value.setStyleSheet(
            'font: italic 9pt "Digital-7 Mono";\n' "font-size: 23px;"
        )
        self.target_value.setAlignment(Qt.AlignCenter)
        self.target_value.setObjectName("target_value")
        self.horizontalLayout_2.addWidget(self.target_value)
        self.verticalLayout_2.addWidget(self.targetFrame)
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.aircon_setting_label = QLabel(self.centralwidget)
        self.aircon_setting_label.setStyleSheet("font-size:10px;")
        self.aircon_setting_label.setObjectName("aircon_setting_label")
        self.verticalLayout_2.addWidget(self.aircon_setting_label)
        self.aircon_value = QLabel(self.centralwidget)
        self.aircon_value.setAlignment(Qt.AlignCenter)
        self.aircon_value.setObjectName("aircon_value")
        self.verticalLayout_2.addWidget(self.aircon_value)
        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_2.addWidget(self.line_5)
        self.lights_label = QLabel(self.centralwidget)
        self.lights_label.setStyleSheet("font-size:10px;")
        self.lights_label.setObjectName("lights_label")
        self.verticalLayout_2.addWidget(self.lights_label)
        self.lights_value = QLabel(self.centralwidget)
        self.lights_value.setStyleSheet(
            "border-radius:10px;\n"
            "border:0.5px solid black;\n"
            "background-color: rgb(255, 241, 38);"
        )
        self.lights_value.setText("")
        self.lights_value.setObjectName("lights_value")
        self.verticalLayout_2.addWidget(self.lights_value)
        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_2.addWidget(self.line_4)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 265, 28))
        self.menuBar.setObjectName("menuBar")
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.setMenuBar(self.menuBar)
        self.actionSettings = QAction(self)
        self.actionSettings.setObjectName("actionSettings")
        self.menuSettings.addAction(self.actionSettings)
        self.menuBar.addAction(self.menuSettings.menuAction())

        self.mode_label.setText(("Mode:"))
        self.unit_details_label.setText(("Dehumidifier Readings:"))
        self.humidity_label.setText(("Humidity:"))
        self.temperature_label.setText(("Temperature:"))
        self.target_label.setText(("Target:"))

        self.aircon_setting_label.setText(("Aircon Setting:"))
        self.lights_label.setText(("Lights:"))
        self.menuSettings.setTitle(("File"))
        self.actionSettings.setText(("Settings"))

        # VARIABLES FOR DATA
        self.unitDataList = []
        self.lightsOnTime = ""
        self.lightsOffTime = ""
        self.modes = ""
        self.areLightsOn = False

        # click triggers
        self.units_combo.currentIndexChanged.connect(self.handleChangeUnitsCombo)
        self.actionSettings.triggered.connect(self.handleOpenSettings)
        self.mode_combo.currentIndexChanged.connect(self.handleModeColorChange)

        # first time function calls
        self.populateModeComboBox()
        self.populateUnitComboBox()
        self.refreshTime()
        self.handleSetLights()
        self.refreshEnvironmentValues()
        self.setEnvironment()
        self.handleSetAirConValue()
        #
        # Threads and Timers
        #
        # set timer for correcting room environment
        self.sendRoomControlTimer = QTimer()
        self.sendRoomControlTimer.setInterval(SEND_ROOM_CONTROL_TIMER_MILLIS)
        # connect timer to function
        self.sendRoomControlTimer.timeout.connect(self.setEnvironment)
        # create thread for timer
        self.sendRoomControlThread = QThread()
        self.sendRoomControlTimer.moveToThread(self.sendRoomControlThread)
        # connect thread to start timer when thread begins.
        self.sendRoomControlThread.started.connect(self.sendRoomControlTimer.start)
        # begin thread
        self.sendRoomControlThread.start()
        #
        #
        #
        # set timer for refresh values
        self.refreshValuesTimer = QTimer()
        self.refreshValuesTimer.setInterval(REFRESH_VALUES_TIMER_MILLIS)  # 12 seconds
        # connect timer to function
        self.refreshValuesTimer.timeout.connect(self.refreshEnvironmentValues)
        # create thread for timer
        self.refreshValuesThread = QThread()
        # move timer to thread
        self.refreshValuesTimer.moveToThread(self.refreshValuesThread)
        # connect thread to start timer when thread begins.
        self.refreshValuesThread.started.connect(self.refreshValuesTimer.start)
        # begin thread
        self.refreshValuesThread.start()
        #
        #
        #

        QMetaObject.connectSlotsByName(self)

    def handleOpenSettings(self):
        settingsUi.exec_()
        return

    def handleChangeUnitsCombo(self):
        dehumidifierUnitList = JSONFileManager(selection="devices").read_json()

        selected_unit = self.units_combo.currentText()
        selected_unit_id = selected_unit[4:5]
        for unit in self.unitDataList:
            if int(unit[0]) == int(selected_unit_id):
                data = unit[1]
                self.humidity_value.setText(f"{data[0]}{degree_symbol}")
                self.target_value.setText(f"{data[1]}{degree_symbol}")
                self.temperature_value.setText(f"{data[2]}{degree_symbol}")
                return

    def refreshEnvironmentValues(self):
        dehumidifierUnitList = JSONFileManager(selection="devices").read_json()

        selected_unit = self.units_combo.currentText()
        selected_unit_id = selected_unit[4:5]

        for unit in dehumidifierUnitList:
            id = unit["id"]
            ip = unit["ip"]
            token = unit["token"]
            try:
                unit = RoomController(ip=ip, token=token)
                active = True

            except:
                active = False
            new_object = {
                "id": id,
                "ip": ip,
                "token": token,
                "active": active,
            }
            JSONFileManager(selection="devices").replace_object_by_id(
                id=id, new_object=new_object
            )
            self.unitDataList.append((id, unit.return_all_sensors(), ip, token, active))

        for device in self.unitDataList:
            if int(selected_unit_id) == int(device[0]):
                data = device[1]
                self.humidity_value.setText(f"{data[0]}{degree_symbol}")
                self.target_value.setText(f"{data[1]}{degree_symbol}")
                self.temperature_value.setText(f"{data[2]}{degree_symbol}")

        if self.areLightsOn:
            self.lights_value.setStyleSheet(style_lights_on)
        else:
            self.lights_value.setStyleSheet(style_lights_off)
        self.refreshTime()
        self.handleSetLights()
        self.handleModeColorChange()

    def handleSetAirConValue(self):
        self.aircon_value.setText((f"#{degree_symbol}"))
        return

    def populateModeComboBox(self):
        settings = JSONFileManager(selection="settings").read_json()
        # unpack values
        humidity_thresholds = settings["humidity_thresholds"]
        self.modes = humidity_thresholds.keys()
        for name in self.modes:
            self.mode_combo.addItem(name.title())
        self.handleModeColorChange()
        return

    def handleModeColorChange(self):
        if self.mode_combo.currentText().lower() == "vegetative":
            self.mode_combo.setStyleSheet("background-color: rgb(144, 238, 144);")
        if self.mode_combo.currentText().lower() == "flowering":
            self.mode_combo.setStyleSheet("background-color: rgb(216, 191, 216);")
        if self.mode_combo.currentText().lower() == "curing":
            self.mode_combo.setStyleSheet("background-color: rgb(240, 230, 140);")
        return

    def populateUnitComboBox(self):
        dehumidifierUnitList = JSONFileManager(selection="devices").read_json()

        if len(dehumidifierUnitList) <= 0:
            self.units_combo.addItem("nothingFoundItem")
            return
        for i, unit in enumerate(dehumidifierUnitList):
            self.units_combo.addItem(f"Id: {unit['id']} - Ip: {unit['ip']}")
        self.units_combo.setCurrentIndex(1)
        return

    def refreshTime(self):
        time_now = datetime.now()
        date_as_int = time_now.day
        month_name = time_now.strftime("%B")
        day_now = time_now.strftime("%A")
        time_now = time_now.strftime("%H:%M:%S")
        date_suffix = "th"

        if date_as_int == 1 or date_as_int == 21 or date_as_int == 31:
            date_suffix = "st"
        elif date_as_int == 2 or date_as_int == 22:
            date_suffix = "nd"
        elif date_as_int == 3 or date_as_int == 23:
            date_suffix = "rd"

        self.day_value.setText(f"{day_now} {date_as_int}{date_suffix}")
        self.month_value.setText(month_name)
        self.time_value.setText(f"{time_now}")
        return

    def handleSetLights(self):
        settings = JSONFileManager(selection="settings").read_json()

        # unpack values
        lights_on_time = settings["lights"]["on"]
        on_hour = lights_on_time["hour"]
        on_minute = lights_on_time["minute"]

        lights_off_time = settings["lights"]["off"]
        off_hour = lights_off_time["hour"]
        off_minute = lights_off_time["minute"]

        # time now
        now = datetime.now().time()
        # set default light strip color
        self.lights_value.setStyleSheet(style_lights_off)
        self.lights_label.setText("Lights: Off")

        # check time
        on_time = dt.time(on_hour, on_minute, 0)
        off_time = dt.time(off_hour, off_minute, 0)

        self.lightsOnTime = on_time
        self.lightsOffTime = off_time
        # Determine whether the lights should be on or off
        if on_time <= now < off_time:
            self.arelightsOn = True
            self.lights_value.setStyleSheet(style_lights_on)
            self.lights_label.setText("Lights: On")
        return

    def setEnvironment(self):
        selectedMode = self.mode_combo.currentText()
        settings = JSONFileManager(selection="settings").read_json()

        dehumidifierUnitList = JSONFileManager(selection="devices").read_json()

        # unpack values
        humidity_thresholds = settings["humidity_thresholds"].items()
        humidity_warning_thresholds = settings["warning_thresholds"]["humidity"]

        for saved_name, saved_targets in humidity_thresholds:
            if saved_name.lower() == selectedMode.lower():
                targets = saved_targets

        for data in self.unitDataList:
            h, tr, t = data[1]
            device_id = data[0]
            ip = data[2]
            token = data[3]
            active = data[4]
            if active == True:
                try:
                    dehumidifier = RoomController(ip=ip, token=token)
                    active = True
                except:
                    active = False

                new_object = {
                    "id": device_id,
                    "ip": ip,
                    "token": token,
                    "active": active,
                }
                JSONFileManager(selection="devices").replace_object_by_id(
                    id=device_id, new_object=new_object
                )
            else:
                try:
                    dehumidifier = RoomController(ip=ip, token=token)
                    active = True
                except:
                    active = False

                new_object = {
                    "id": device_id,
                    "ip": ip,
                    "token": token,
                    "active": active,
                }
                JSONFileManager(selection="devices").replace_object_by_id(
                    id=device_id, new_object=new_object
                )
            # # humidity good
            if h >= targets["low"] and h <= targets["high"]:
                pass

            # humidity too low
            if h < targets["low"]:
                if tr == UNIT_HUMIDITY_TARGETS["low"]:
                    response = dehumidifier.set_target(UNIT_HUMIDITY_TARGETS["high"])

            # humidity too high
            elif h > targets["high"]:
                if tr == UNIT_HUMIDITY_TARGETS["high"]:
                    response = dehumidifier.set_target(UNIT_HUMIDITY_TARGETS["low"])

            elif h <= humidity_warning_thresholds["low"]:
                response = dehumidifier.set_target(UNIT_HUMIDITY_TARGETS["high"])

            elif h >= humidity_warning_thresholds["high"]:
                response = dehumidifier.set_target(UNIT_HUMIDITY_TARGETS["low"])
        return


app = QApplication(sys.argv)
ui = TheMainWindow()
