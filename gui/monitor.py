import time
import cv2 as cv
import numpy as np

from PySide6.QtCore import QMetaObject, QCoreApplication, Slot, Qt, QTimer
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QWidget
from PySide6.QtGui import QImage, QPixmap


class Monitor(QWidget):

    def __init__(self, camera, parent):
        super(Monitor, self).__init__(parent)
        print("初始化显示界面···")
        self.cam = camera
        self.cap_flag = True
        self.get_frame_timer = QTimer()
        self.get_frame_timer.timeout.connect(self.get_frame)
        self.setObjectName(u"Display")
        self.resize(340, 371)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startCapture = QPushButton(self)
        self.startCapture.setObjectName(u"startCapture")

        self.horizontalLayout.addWidget(self.startCapture)

        self.singleFrameCap = QPushButton(self)
        self.singleFrameCap.setObjectName(u"singleFrameCap")

        self.horizontalLayout.addWidget(self.singleFrameCap)

        self.stopCapture = QPushButton(self)
        self.stopCapture.setObjectName(u"stopCapture")

        self.horizontalLayout.addWidget(self.stopCapture)

        self.saveToVideo = QPushButton(self)
        self.saveToVideo.setObjectName(u"saveToVideo")

        self.horizontalLayout.addWidget(self.saveToVideo)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.displayWindow = QLabel(self)
        self.displayWindow.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayWindow.sizePolicy().hasHeightForWidth())
        self.displayWindow.setSizePolicy(sizePolicy)
        self.displayWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.startCapture.setEnabled(True)
        self.stopCapture.setEnabled(False)
        self.startCapture.clicked.connect(self.start_cap)
        self.stopCapture.clicked.connect(self.stop_cap)

        self.verticalLayout.addWidget(self.displayWindow)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslate()
        self.load_wallpaper()

        QMetaObject.connectSlotsByName(self)

    def retranslate(self):
        self.setWindowTitle(QCoreApplication.translate("Display", u"Form", None))
        self.startCapture.setText(QCoreApplication.translate("Display", u"\u542f\u52a8", None))
        self.singleFrameCap.setText(QCoreApplication.translate("Display", u"\u5355\u5e27\u83b7\u53d6", None))
        self.stopCapture.setText(QCoreApplication.translate("Display", u"\u505c\u6b62", None))
        self.saveToVideo.setText(QCoreApplication.translate("Display", u"\u5f55\u5236", None))
        self.displayWindow.setText("")

    def load_wallpaper(self):
        wallpaper = cv.imread("./static/wallpaper.png")
        h, w, ch = wallpaper.shape
        wallpaper = QImage(wallpaper, w, h, ch * w, QImage.Format_RGB888)
        wallpaper = wallpaper.scaled(612, 512, Qt.KeepAspectRatio)
        self.displayWindow.setPixmap(QPixmap.fromImage(wallpaper))

    def set_image(self, image):

        if isinstance(image, np.ndarray):
            h, w, ch = image.shape
            image = QImage(image, w, h, ch * w, QImage.Format_RGB888)
            image = image.scaled(640, 480, Qt.KeepAspectRatio)

        self.displayWindow.setPixmap(QPixmap.fromImage(image))

    @Slot()
    def start_cap(self):
        print("开始采集数据！")
        if self.cam.current_cam == None:
            print("找不到当前相机或未选择相机！")
        self.startCapture.setEnabled(False)
        self.stopCapture.setEnabled(True)
        self.get_frame_timer.start(50)

    @Slot()
    def get_frame(self):
        self.cam.get_frame()
        frame = self.cam.buffer.pop()
        self.set_image(frame)

    @Slot()
    def stop_cap(self):
        self.cap_flag = False
        self.stopCapture.setEnabled(False)
        self.startCapture.setEnabled(True)
        self.get_frame_timer.stop()
        self.cam.stop()