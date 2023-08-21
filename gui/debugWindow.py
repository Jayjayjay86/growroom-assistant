import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

UPDATE_DEBUG_WINDOW_MILLIS = 90000


class DebugWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(365, 355)
        self.setWindowTitle("Debug Window")
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.terminalTextEdit = QPlainTextEdit(self)
        self.terminalTextEdit.setObjectName("terminalTextEdit")
        self.verticalLayout.addWidget(self.terminalTextEdit)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        #
        # Set timer for updating debug window.
        self.debugWindowTimer = QTimer()
        self.debugWindowTimer.setInterval(UPDATE_DEBUG_WINDOW_MILLIS)
        # connect timer to function
        self.debugWindowTimer.timeout.connect(self.handleUpdateDebugWindow)
        # create thread for timer
        self.debugWindowThread = QThread()
        self.debugWindowTimer.moveToThread(self.debugWindowThread)
        # connect thread to start timer when thread begins.
        self.debugWindowThread.started.connect(self.debugWindowTimer.start)
        # begin thread
        self.debugWindowThread.start()
        #
        #
        QMetaObject.connectSlotsByName(self)

    def handleUpdateDebugWindow(self):
        pass


debugWindowApp = QApplication(sys.argv)
debugWindowUi = DebugWindow()
