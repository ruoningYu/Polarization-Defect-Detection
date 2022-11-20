# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import sys


from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from gui.main_window import Ui_MainWindow


if __name__ == "__main__":

    app = QApplication()
    main = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupMainWindowUi(main)
    main.show()
    sys.exit(app.exec())
