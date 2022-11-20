# -*- coding: utf-8 -*-

import sys
import PySpin

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *

from camera import Camera
from thread_manager import CaptureThread, ShowThread

from .device_controller import DeviceController
from .device_list import DeviceList
from .log_viewer import LogViewer
from .monitor import Monitor


class Ui_MainWindow(object):

    def __init__(self):
        self.cam = Camera()
        self.capThread = CaptureThread()
        self.showThread = ShowThread()

    def setupMainWindowUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 700)

        self.actionHELP = QAction(MainWindow)
        self.actionHELP.setObjectName(u"actionHELP")
        self.actionABOUT = QAction(MainWindow)
        self.actionABOUT.setObjectName(u"actionABOUT")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionHELP)
        self.menu.addAction(self.actionABOUT)

        self.mainWindowVerticalLayout = QVBoxLayout()
        self.mainWindowVerticalLayout.setObjectName(u'mainWindowVerticalLayout')

        self.mainWindowHorizontalLayoutTop = QHBoxLayout()
        self.mainWindowHorizontalLayoutTop.setObjectName(u'mainWindowHorizontalLayoutTop')

        self.mainWindowRightVerticalLayoutInHorizontalLayoutTop = QVBoxLayout()
        self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.setObjectName(
            u'mainWindowVerticalLayoutInHorizontalLayoutTop')

        self.mainWindowHorizontalLayoutTop.addLayout(self.mainWindowRightVerticalLayoutInHorizontalLayoutTop)

        self.mainWindowVerticalLayout.addLayout(self.mainWindowHorizontalLayoutTop)

        self.centralwidget.setLayout(self.mainWindowVerticalLayout)
        # 装载组件界面
        self.loadModuleUi()
        self.retranslate(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def refreshDisplayUi(self, nodemap_dict):
        for key, value in nodemap_dict.item():
            try:
                type = nodemap_dict["type"]
            except KeyError:
                pass

    def retranslate(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", u"\u7acb\u654f\u8fbe\u7f3a\u9677\u68c0\u6d4b\u7cfb\u7edf", None))
        self.actionHELP.setText(QCoreApplication.translate("MainWindow", u"HELP", None))
        self.actionABOUT.setText(QCoreApplication.translate("MainWindow", u"ABOUT", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))

    def loadModuleUi(self):
        self.device_list_ui = DeviceList(self.cam)
        self.device_controller_ui = DeviceController(self.cam)
        self.monitor_ui = Monitor(self.cam)
        self.log_viewer_ui = LogViewer()

        self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.addWidget(self.device_list_ui)
        self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.addWidget(self.device_controller_ui)
        self.mainWindowHorizontalLayoutTop.addWidget(self.monitor_ui)
        self.mainWindowVerticalLayout.addWidget(self.log_viewer_ui)

        self.device_list_ui.setup(QWidget())
        self.device_controller_ui.setup(QWidget())
        self.monitor_ui.setup(QWidget())
        self.log_viewer_ui.setup(QWidget())


# usage
if __name__ == "__main__":
    app = QApplication()
    main = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupMainWindowUi(main)
    main.show()
    sys.exit(app.exec())
