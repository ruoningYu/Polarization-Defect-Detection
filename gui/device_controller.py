from PySide6.QtCore import (QMetaObject, QCoreApplication, QStringListModel)
from PySide6.QtGui import (QStandardItemModel, QStandardItem)
from PySide6.QtWidgets import (QSizePolicy, QHBoxLayout, QVBoxLayout, QTabWidget, QWidget, QListView, QTreeView,
                               QHeaderView)


class DeviceController(QWidget):

    def __init__(self, camera=None, parent=None):
        super(DeviceController, self).__init__(parent)
        self.cam = camera
        print("初始化设备控制台···")

        self.setObjectName(u"Form")
        self.resize(500, 500)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # Form.setMaximumSize(QSize(500, 500))
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.tabWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslate(self)
        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self)

    def retranslate(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))

    def base_feature_tab(self):
        cameraBaseInfoTab = QWidget()
        cameraBaseInfoTab.setObjectName(u"baseInfoTab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(cameraBaseInfoTab.sizePolicy().hasHeightForWidth())
        cameraBaseInfoTab.setSizePolicy(sizePolicy1)

        verticalLayout = QVBoxLayout(cameraBaseInfoTab)
        verticalLayout.setObjectName(u"verticalLayout_baseinfo")

        baseinfo_tree = QListView()

        listmodel = QStringListModel()
        listmodel.setStringList(self.device_info_list)
        verticalLayout.addWidget(baseinfo_tree)

        baseinfo_tree.setModel(listmodel)

        self.tabWidget.addTab(cameraBaseInfoTab, "相机基本信息")

    def refresh_feature_data(self):
        tab = QWidget()
        tab.setObjectName(u'tabObject')

        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(tab.sizePolicy().hasHeightForWidth())
        tab.setSizePolicy(sizePolicy1)

        verticalLayout = QVBoxLayout(tab)
        verticalLayout.setObjectName(u"verticalLayoutTab")

        control_feature_tree = QTreeView(tab)
        verticalLayout.addWidget(control_feature_tree)

        feature_model = self.get_feature_model()
        control_feature_tree.setModel(feature_model)
        control_feature_tree.header().setSectionResizeMode(QHeaderView.Stretch)
        control_feature_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.base_feature_tab()
        self.tabWidget.addTab(tab, "相机参数控制")

    def get_feature_model(self):
        node_map = self.cam.get_node_map()
        feature_model = QStandardItemModel()
        for layer in node_map:
            layer_model = QStandardItem(layer)
            feature_model.appendRow(layer_model)
            feature_model.setHorizontalHeaderLabels(['NAME', 'VALUE'])
            for category in node_map[layer]['Root']:
                device_info_flag = False
                category_model = QStandardItem(category)
                category_model.setColumnCount(2)
                layer_model.appendRow(category_model)
                layer_model.setChild(0, 1, QStandardItem())
                if category == 'Device Information':
                    self.device_info_list = list()
                    device_info_flag = True

                n = 0
                for item in node_map[layer]['Root'][category]:
                    try:
                        node = node_map[layer]['Root'][category][item]
                        node_type = node_map[layer]['Root'][category][item]['type']
                    except KeyError:
                        continue
                    node_value = node['value'] if ('value' in node) else node['tooltip'] \
                        if ('tooltip' in node) else node['entry_symbolic']
                    try:
                        if node_type == "string":
                            node_item = QStandardItem(item)
                            node_value_item = QStandardItem(str(node_value))
                        elif node_type == "integer":
                            node_item = QStandardItem(item)
                            node_value_item = QStandardItem(str(node_value))
                        elif node_type == "float":
                            node_item = QStandardItem(item)
                            node_value_item = QStandardItem(str(node_value))
                        elif node_type == "command":
                            node_item = QStandardItem(item)
                            node_value_item = QStandardItem(str(node_value))
                        elif node_type == "enumeration":
                            node_item = QStandardItem(item)
                            node_value_item = QStandardItem(str(node_value))
                        elif node_type == "boolean":
                            node_item = QStandardItem(item)
                            node_value_item = QStandardItem(str(node_value))
                        # print(n, item, node_value)
                        category_model.appendRow(node_item)
                        category_model.setChild(node_item.index().row(), 1, node_value_item)
                        n += 1
                    except OverflowError:
                        raise print(node)
                    if device_info_flag:
                        self.device_info_list.append(item + ":    " + str(node_value))

        return feature_model
