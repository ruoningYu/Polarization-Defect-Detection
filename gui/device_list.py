from PySide6.QtCore import (QMetaObject, Qt, QCoreApplication, Slot)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QSizePolicy, QHBoxLayout, QStyleFactory, QWidget,
                               QVBoxLayout, QPushButton, QTreeView, QHeaderView)

from device_controller import DeviceController


class DeviceList(QWidget):

    def __init__(self, camera, parent=None):
        super(DeviceList, self).__init__()
        self.cam = camera
        self.parent = parent
        print("初始化设备列表···")

        self.setObjectName(u"DeviceInfo")
        self.setWindowModality(Qt.NonModal)
        self.resize(300, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.refleshDeviceButton = QPushButton()
        self.refleshDeviceButton.clicked.connect(self.choose_camera)

        self.CameraInfo = QTreeView(self)
        self.CameraInfo.setObjectName(u"treeView")

        self.verticalLayout.addWidget(self.CameraInfo)
        self.verticalLayout.addWidget(self.refleshDeviceButton)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslate(self)

        QMetaObject.connectSlotsByName(self)

    def retranslate(self, DeviceInfo):
        self.refleshDeviceButton.setText(
            QCoreApplication.translate("Display", u"\u5237\u65b0\u8bbe\u5907\u5217\u8868", None))
        DeviceInfo.setWindowTitle(QCoreApplication.translate("DeviceInfo", u"\u8bbe\u5907\u5217\u8868", None))

    @Slot()
    def choose_camera(self):
        interface_model = self.cam.get_interface_model()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['相机列表'])
        itemList = QStandardItem('接口信息')
        model.appendRow(itemList)
        # model.setItem(0, 1, QStandardItem('设备信息'))
        for key in interface_model:
            interface = QStandardItem(key)
            itemList.appendRow(interface)
            for i in range(len(interface_model[key])):
                device = interface_model[key][i]
                _device = QStandardItem(device[0])
                interface.appendRow(_device)
                interface.setChild(0, 0, QStandardItem(" ".join(device[1:])))

        self.CameraInfo.setModel(model)
        # 调整第一列的宽度
        # self.CameraInfo.header().resizeSection(0, 300)
        # 设置成有虚线连接的方式
        self.CameraInfo.setStyle(QStyleFactory.create('windows'))
        # 全部展开
        self.CameraInfo.expandAll()
        self.CameraInfo.selectionModel().currentChanged.connect(self.load_cam_info)
        self.CameraInfo.header().setSectionResizeMode(QHeaderView.Stretch)
        self.CameraInfo.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    def load_cam_info(self, cam_id):
        controller = DeviceController(self.cam)
        self.cam.select_camera(cam_id)
        self.cam.setup_cap()
        controller.refresh_feature_data()
        self.parent.load_current_cam_info(controller)
