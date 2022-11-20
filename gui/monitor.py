from PySide6.QtCore import QMetaObject, QCoreApplication, Slot
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PySide6.QtGui import QImage, QPixmap


class Monitor:

    def __init__(self, camera):
        self.cam = camera

    def setup(self, monitor):
        print("初始化显示界面···")
        if not monitor.objectName():
            monitor.setObjectName(u"Display")
        monitor.resize(340, 371)
        self.verticalLayout_2 = QVBoxLayout(monitor)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startCapture = QPushButton(monitor)
        self.startCapture.setObjectName(u"startCapture")

        self.horizontalLayout.addWidget(self.startCapture)

        self.singleFrameCap = QPushButton(monitor)
        self.singleFrameCap.setObjectName(u"singleFrameCap")

        self.horizontalLayout.addWidget(self.singleFrameCap)

        self.stopCapture = QPushButton(monitor)
        self.stopCapture.setObjectName(u"stopCapture")

        self.horizontalLayout.addWidget(self.stopCapture)

        self.saveToVideo = QPushButton(monitor)
        self.saveToVideo.setObjectName(u"saveToVideo")

        self.horizontalLayout.addWidget(self.saveToVideo)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.displayWindow = QLabel(monitor)
        self.displayWindow.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayWindow.sizePolicy().hasHeightForWidth())
        self.displayWindow.setSizePolicy(sizePolicy)
        self.displayWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.startCapture.setEnabled(True)
        self.stopCapture.setEnabled(False)
        self.startCapture.clicked.connect(self.start)
        self.stopCapture.clicked.connect(self.stop)

        self.verticalLayout.addWidget(self.displayWindow)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslate(monitor)

        QMetaObject.connectSlotsByName(monitor)

    def retranslate(self, Display):
        Display.setWindowTitle(QCoreApplication.translate("Display", u"Form", None))
        self.startCapture.setText(QCoreApplication.translate("Display", u"\u542f\u52a8", None))
        self.singleFrameCap.setText(QCoreApplication.translate("Display", u"\u5355\u5e27\u83b7\u53d6", None))
        self.stopCapture.setText(QCoreApplication.translate("Display", u"\u505c\u6b62", None))
        self.saveToVideo.setText(QCoreApplication.translate("Display", u"\u5f55\u5236", None))
        self.displayWindow.setText("")

    @Slot(QImage)
    def setImage(self, image):
        self.displayWindow.setPixmap(QPixmap.fromImage(image))

    @Slot()
    def start(self):
        # todo 不在直接从camera中获取图像而是从Camera类中获取图像

        if self.cam.current_cam == None:
            print("找不到当前相机或未选择相机！")
        self.startCapture.setEnabled(False)
        self.stopCapture.setEnabled(True)
        self.capThread.init_camera(self.currentCam)
        self.nodemap = CameraNodeMap(self.currentCam)
        self.nodemap_dict = self.nodemap.get_whole_nodemap()

        self.showThread.set_buffer(self.capThread.get_buffer)
        self.showThread.updateFrame.connect(self.setImage)
        self.capThread.start()
        self.showThread.start()

    @Slot()
    def stop(self):
        self.stopCapture.setEnabled(False)
        self.startCapture.setEnabled(True)
        self.capThread.terminate()
        self.showThread.terminate()
