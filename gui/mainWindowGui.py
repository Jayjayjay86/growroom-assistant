import sys
from datetime import datetime
import datetime as dt
from logic.jsonFileManager import JSONFileManager
from logic.roomControl import RoomController
from gui.settingsUi import settingsUi, settingsApp
import logging
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from logic.logging import makeLog

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

HANDLE_ACTIVE_DEHUMIDIFIERS_TIME_MILLIS = 120000
HANDLE_DEHUMDIFIER_DATA_TIME_MILLIS = 12000
HANDLE_SEND_COMMANDS_TIME_MILLIS = 90000

UNIT_HUMIDITY_extracted_TARGETS = {"low": 60, "high": 70}


class TheMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # debug messages
        self.debug_messages = []
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
        self.menuBar.setGeometry(QRect(0, 0, 265, 20))
        self.menuBar.setObjectName("menuBar")
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")

        self.setMenuBar(self.menuBar)
        self.actionSettings = QAction(self)
        self.actionSettings.setObjectName("actionSettings")
        self.actionDebug_Window = QAction(self)
        self.actionDebug_Window.setObjectName("actionDebug_Window")
        self.actionDebug_Window.setCheckable(True)
        self.actionDebug_Window.setChecked(False)
        self.menuSettings.addAction(self.actionSettings)
        self.menuSettings.addAction(self.actionDebug_Window)
        self.menuBar.addAction(self.menuSettings.menuAction())

        # render text to display on screen
        self.mode_label.setText(("Mode:"))
        self.unit_details_label.setText(("Dehumidifier Readings:"))
        self.humidity_label.setText(("Humidity:"))
        self.temperature_label.setText(("Temperature:"))
        self.target_label.setText(("Target:"))
        self.aircon_setting_label.setText(("Aircon Setting:"))
        self.lights_label.setText(("Lights:"))
        self.menuSettings.setTitle(("File"))
        self.actionSettings.setText("Settings")
        self.actionDebug_Window.setText("Debug")

        # VARIABLES FOR DATA
        self.active_dehumidifier_list = []
        self.lightsOnTime = ""
        self.lightsOffTime = ""
        self.modes = ""
        self.areLightsOn = False
        self.debug_messages.append("testing triggers")

        # click triggers
        self.units_combo.currentIndexChanged.connect(self.handleRefreshDehumidifierData)
        self.actionSettings.triggered.connect(self.handleOpenSettings)
        self.actionDebug_Window.triggered.connect(self.toggle_debug)
        self.mode_combo.currentIndexChanged.connect(self.handleModeColorChange)

        # first time function calls
        self.debug_messages.append("refreshing screen")

        self.handleRefreshTime()
        self.handleModeComboBox()
        self.handleUnitComboBox()
        self.handleSetAirConValue()
        self.handleLightColors()
        self.handleActiveDehumidifiersList()
        self.handleRefreshDehumidifierData()
        self.debug_messages.append("setting timers and threads")

        #
        # Threads and Timers
        #
        # set timer for correcting room environment
        self.handleSendCommandsTimer = QTimer()
        self.handleSendCommandsTimer.setInterval(HANDLE_SEND_COMMANDS_TIME_MILLIS)
        # connect timer to function
        self.handleSendCommandsTimer.timeout.connect(self.handleSendCommands)
        # create thread for timer
        self.handleSendCommandsThread = QThread()
        self.handleSendCommandsTimer.moveToThread(self.handleSendCommandsThread)
        # connect thread to start timer when thread begins.
        self.handleSendCommandsThread.started.connect(
            self.handleSendCommandsTimer.start
        )
        # begin thread
        self.handleSendCommandsThread.start()
        #
        #
        #
        # Set timer for updating duhumidifier value data.
        self.updateDehumidifierDataTimer = QTimer()
        self.updateDehumidifierDataTimer.setInterval(
            HANDLE_DEHUMDIFIER_DATA_TIME_MILLIS
        )
        # connect timer to function
        self.updateDehumidifierDataTimer.timeout.connect(
            self.handleRefreshDehumidifierData
        )
        # create thread for timer
        self.updateDehumidifierDataThread = QThread()
        self.updateDehumidifierDataTimer.moveToThread(self.updateDehumidifierDataThread)
        # connect thread to start timer when thread begins.
        self.updateDehumidifierDataThread.started.connect(
            self.updateDehumidifierDataTimer.start
        )
        # begin thread
        self.updateDehumidifierDataThread.start()
        #
        #

        #
        # # Set timer for putting active dehumidifers into the list.
        # self.handleActiveDehumidifiersListTimer = QTimer()
        # self.handleActiveDehumidifiersListTimer.setInterval(
        #     HANDLE_ACTIVE_DEHUMIDIFIERS_TIME_MILLIS
        # )
        # # connect timer to function
        # self.handleActiveDehumidifiersListTimer.timeout.connect(
        #     self.handleActiveDehumidifiersList
        # )
        # # create thread for timer
        # self.handleActiveDehumidifiersListThread = QThread()
        # # move timer to thread
        # self.handleActiveDehumidifiersListTimer.moveToThread(
        #     self.handleActiveDehumidifiersListThread
        # )
        # # connect thread to start timer when thread begins.
        # self.handleActiveDehumidifiersListThread.started.connect(
        #     self.handleActiveDehumidifiersListTimer.start
        # )
        # # begin thread
        # self.handleActiveDehumidifiersListThread.start()
        # #
        # #
        # #
        self.debug_messages.append("connecting slots")
        QMetaObject.connectSlotsByName(self)

    def handleSendCommands(self):
        # Requested mode from mode combo-box.
        selectedMode = self.mode_combo.currentText()
        # Open settings
        settings = JSONFileManager(selection="settings").read_json()

        # unpack values
        humidity_thresholds = settings["humidity_thresholds"].items()
        humidity_warning_thresholds = settings["warning_thresholds"]["humidity"]

        for mode, targets in humidity_thresholds:
            if mode.lower() == selectedMode.lower():
                extracted_targets = targets

        if len(self.active_dehumidifier_list) <= 0:
            return
        self.debug_messages.append(("active list:", len(self.active_dehumidifier_list)))

        for data in self.active_dehumidifier_list:
            device_id = data[0]
            ip = data[1]
            token = data[2]

            # Connect to dehumidiifer
            self.debug_messages.append("establishing conection")
            dehumidifier = RoomController(ip=ip, token=token)
            # Check humidity against targets.
            self.debug_messages.append("checking humidity")

            # humidity good
            self.debug_messages.append("connecting to unit")

            h, tr, t = dehumidifier.return_all_sensors()
            if h >= extracted_targets["low"] and h <= extracted_targets["high"]:
                continue

            # humidity too low
            if h < extracted_targets["low"]:
                if tr == UNIT_HUMIDITY_extracted_TARGETS["low"]:
                    # Issue command
                    dehumidifier.set_target(UNIT_HUMIDITY_extracted_TARGETS["high"])

            # humidity too high
            elif h > extracted_targets["high"]:
                if tr == UNIT_HUMIDITY_extracted_TARGETS["high"]:
                    # Issue command
                    dehumidifier.set_target(UNIT_HUMIDITY_extracted_TARGETS["low"])

            # Check warning levels (possible air-con intervention to control).
            elif h <= humidity_warning_thresholds["low"]:
                # Issue command
                dehumidifier.set_target(UNIT_HUMIDITY_extracted_TARGETS["high"])
                self.debug_messages.append("warning humidity too low")

            elif h >= humidity_warning_thresholds["high"]:
                # Issue command
                dehumidifier.set_target(UNIT_HUMIDITY_extracted_TARGETS["low"])
                self.debug_messages.append("warning humidity too high")

            self.debug_messages.append("finished checks")

            # # clear list
            # self.active_dehumidifier_list=[]

    def handleRefreshDehumidifierData(self):
        self.debug_messages.append("refreshing screen with stored values")
        for unit in self.active_dehumidifier_list:
            # Try to connect with the dehumidifier using extracted ip and token.
            dehumidifier = RoomController(ip=unit[1], token=unit[2])
            data = dehumidifier.return_all_sensors()
            try:
                h, t, tr = data
            except:
                print(data)
                h, tr, t = 0, 0, 0
                logging.warning("device couldn't be located")
            # Add dehumidifier to list.

            if int(unit[0]) == int(self.units_combo.currentText()[4:5]):
                self.humidity_value.setText(f"{h}{degree_symbol}")
                self.target_value.setText(f"{tr}{degree_symbol}")
                self.temperature_value.setText(f"{t}{degree_symbol}")
                return

    def handleActiveDehumidifiersList(self):
        self.debug_messages.append("checking active units")

        # Open and parse dehumidifier list.
        dehumidifiersList = JSONFileManager(selection="devices").read_json()

        # Iterate the list, filtering out inactive dehumidifiers.
        # Append active dehumidifiers to the active list.
        for unit in dehumidifiersList:
            # Try to connect with the dehumidifier using extracted ip and token.
            if unit["active"] == True:
                dehumidifier = RoomController(ip=unit["ip"], token=unit["token"])
                data = dehumidifier.return_all_sensors()
                if data == 0:
                    unit["active"] = False
                    JSONFileManager(selection="devices").replace_object_by_id(
                        unit["id"],
                        new_object={
                            "id": unit["id"],
                            "ip": unit["ip"],
                            "token": unit["token"],
                            "active": False,
                        },
                    )
                else:
                    # Add dehumidifier to list.
                    self.debug_messages.append(str(len(self.active_dehumidifier_list)))

                    if len(self.active_dehumidifier_list) == 0:
                        self.active_dehumidifier_list.append(
                            (
                                unit["id"],
                                unit["ip"],
                                unit["token"],
                            )
                        )
                        continue
                    if unit["id"] in (
                        entry[0] for entry in self.active_dehumidifier_list
                    ):
                        continue

                    self.active_dehumidifier_list.append(
                        (
                            unit["id"],
                            unit["ip"],
                            unit["token"],
                        )
                    )

            self.debug_messages.append("skipping disconnected unit")

            continue

    def handleLightColors(self):
        # Open settings file.
        settings = JSONFileManager(selection="settings").read_json()

        # Unpack values.
        lights_on_time = settings["lights"]["on"]
        on_hour = lights_on_time["hour"]
        on_minute = lights_on_time["minute"]

        lights_off_time = settings["lights"]["off"]
        off_hour = lights_off_time["hour"]
        off_minute = lights_off_time["minute"]

        # Get the time now.
        now = datetime.now().time()
        # Set default light strip color
        self.lights_value.setStyleSheet(style_lights_off)
        self.lights_label.setText("Lights: Off")

        # Check times
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

    def handleUnitComboBox(self):
        # Clear box
        self.units_combo.clear()
        # Open dehumidifier list
        dehumidifiersList = JSONFileManager(selection="devices").read_json()

        # If list empty display empty message.
        if len(dehumidifiersList) <= 0:
            self.units_combo.addItem("Nothing Found!")
            return
        # Display details of dehumidifiers in the combo-box.
        for i, unit in enumerate(dehumidifiersList):
            if unit["active"] == True:
                self.units_combo.addItem(f"Id: {unit['id']} - Ip: {unit['ip']}")
        # Set the index of the combo-box to first
        self.units_combo.setCurrentIndex(0)
        return

    def handleModeComboBox(self):
        # Open settings config
        settings = JSONFileManager(selection="settings").read_json()
        # Unpack values
        humidity_thresholds = settings["humidity_thresholds"]
        # Get names from settings of modes
        self.modes = humidity_thresholds.keys()
        # Apply name to combo-box.
        for name in self.modes:
            self.mode_combo.addItem(name.title())
        # Change color of combo-box to match current selection
        return

    def toggle_debug(self):
        debug_mode_enabled = self.actionDebug_Window.isChecked()
        # Update logging level based on debug mode
        if debug_mode_enabled:
            makeLog()  # Initialize logging if not already initialized
            logging.getLogger().setLevel(logging.DEBUG)

            logging.debug("Debug mode enabled")
            self.show_warning_box(title="Debug Mode:", warning="Debug mode enabled")
        else:
            logging.getLogger().setLevel(logging.WARNING)
            logging.debug("Debug mode disabled")
            self.show_warning_box(title="Debug Mode:", warning="Debug mode disabled")
        # Update the checked state of the menu item only once at the end
        self.actionDebug_Window.setChecked(debug_mode_enabled)

    def handleOpenSettings(self):
        settingsUi.exec_()

    def handleSetAirConValue(self):
        self.aircon_value.setText((f"# {degree_symbol}"))

    def handleModeColorChange(self):
        if self.mode_combo.currentText().lower() == "vegetative":
            self.mode_combo.setStyleSheet("background-color: rgb(144, 238, 144);")
        if self.mode_combo.currentText().lower() == "flowering":
            self.mode_combo.setStyleSheet("background-color: rgb(216, 191, 216);")
        if self.mode_combo.currentText().lower() == "curing":
            self.mode_combo.setStyleSheet("background-color: rgb(240, 230, 140);")

    def handleRefreshTime(self):
        # Get time now and extract nessesary values.
        time_now = datetime.now()
        date_as_int = time_now.day
        month_name = time_now.strftime("%B")
        day_now = time_now.strftime("%A")
        time_now = time_now.strftime("%H:%M:%S")
        # Apply date suffix
        date_suffix = "th"

        if date_as_int == 1 or date_as_int == 21 or date_as_int == 31:
            date_suffix = "st"
        elif date_as_int == 2 or date_as_int == 22:
            date_suffix = "nd"
        elif date_as_int == 3 or date_as_int == 23:
            date_suffix = "rd"
        # Set values on screen
        self.day_value.setText(f"{day_now} {date_as_int}{date_suffix}")
        self.month_value.setText(month_name)
        self.time_value.setText(f"{time_now}")
        return

    def show_warning_box(self, title, warning):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(warning)
        msg_box.exec_()


app = QApplication(sys.argv)
ui = TheMainWindow()
