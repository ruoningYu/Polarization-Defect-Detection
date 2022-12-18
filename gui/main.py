# -*- coding: utf-8 -*-

import sys
import os

from PySide6.QtCore import (QCoreApplication, QMetaObject, Slot, QRect)
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QMenuBar,
                               QMenu, QStatusBar, QVBoxLayout, QHBoxLayout)

from defectdetector.camera import Camera
from device_list import DeviceList
from log_viewer import LogViewer
from monitor import Monitor
from AboutBox import About


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        config = "config/FLIR_BFS_US_51S5P.json"
        self.cam = Camera(config)
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.resize(1000, 700)

        self.actionHELP = QAction(self)
        self.actionHELP.setObjectName(u"actionHELP")
        self.actionABOUT = QAction(self)
        self.actionABOUT.setObjectName(u"actionABOUT")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName(u"statusBar")
        self.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionHELP)
        self.menu.addAction(self.actionABOUT)

        self.mainWindowVerticalLayout = QVBoxLayout()
        self.mainWindowVerticalLayout.setObjectName(
            u'mainWindowVerticalLayout')

        self.mainWindowHorizontalLayoutTop = QHBoxLayout()
        self.mainWindowHorizontalLayoutTop.setObjectName(
            u'mainWindowHorizontalLayoutTop')

        self.mainWindowRightVerticalLayoutInHorizontalLayoutTop = QVBoxLayout()
        self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.setObjectName(
            u'mainWindowVerticalLayoutInHorizontalLayoutTop')

        self.mainWindowHorizontalLayoutTop.addLayout(
            self.mainWindowRightVerticalLayoutInHorizontalLayoutTop)
        self.mainWindowVerticalLayout.addLayout(
            self.mainWindowHorizontalLayoutTop)
        self.centralwidget.setLayout(self.mainWindowVerticalLayout)

        # 连接信号槽
        self.actionABOUT.triggered.connect(self.ClickABOUT)
        self.actionHELP.triggered.connect(self.ClickHELP)

        # 装载组件界面
        self.load_module_ui()
        self.retranslate()

        QMetaObject.connectSlotsByName(self)

    def retranslate(self):
        self.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", u"\u7f3a\u9677\u68c0\u6d4b\u7cfb\u7edf", None))
        self.actionHELP.setText(
            QCoreApplication.translate("MainWindow", u"HELP", None))
        self.actionABOUT.setText(
            QCoreApplication.translate("MainWindow", u"ABOUT", None))
        self.menu.setTitle(QCoreApplication.translate(
            "MainWindow", u"\u5e2e\u52a9", None))

    def load_module_ui(self):
        self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.addWidget(
            DeviceList(self.cam, self))
        self.mainWindowHorizontalLayoutTop.addWidget(Monitor(self.cam, self))
        self.mainWindowVerticalLayout.addWidget(LogViewer(self))

    def load_current_cam_info(self, device_info_ui):
        if self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.count() < 2:
            self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.addWidget(
                device_info_ui)
        else:
            self.mainWindowRightVerticalLayoutInHorizontalLayoutTop.replaceWidget(
                device_info_ui, device_info_ui)

    @Slot()
    def ClickABOUT(self):
        print('About Button')
        self.AboutBox = About()
        self.AboutBox.show()

    @Slot()
    def ClickHELP(self):
        print('Help Button')


# usage
if __name__ == "__main__":
    app = QApplication()
    main = Ui_MainWindow()
    main.show()
    sys.exit(app.exec())
