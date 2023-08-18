import sys
from gui.mainWindowGui import ui, app
from gui.settingsUi import settingsUi, settingsApp
from logic.jsonFileManager import JSONFileManager
from PyQt5.QtWidgets import QDialog

if __name__ == "__main__":
    units = JSONFileManager(selection="devices").read_json()
    if len(units) <= 0:
        settingsApp = sys.argv
        confirm = settingsUi.exec_()
        settingsApp.exec_()
        if confirm == QDialog.Accepted:
            ui.show()
            sys.exit(app.exec_())
        sys.exit()

    # start program normally
    ui.show()
    sys.exit(app.exec_())
