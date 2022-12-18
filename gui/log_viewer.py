from PySide6.QtCore import (QMetaObject, QCoreApplication, Slot)
from PySide6.QtWidgets import (QSizePolicy, QHBoxLayout, QVBoxLayout,
                               QToolButton, QSpacerItem, QWidget,
                               QTableView, QHeaderView)
from PySide6.QtGui import QStandardItemModel, QStandardItem

from defectdetector.logger.record_buffer import RecordBuffer


class LogViewer(QWidget):

    buffer_size = 0

    def __init__(self, parent):
        super(LogViewer, self).__init__(parent)
        print("初始化日志显示器···")

        log_buffer = RecordBuffer()
        log_buffer.record_signal.connect(self.update_log)

        self.setObjectName(u"Form")
        self.resize(400, 300)
        self.setMaximumHeight(300)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.tableView = QTableView(self)
        self.tableView.setObjectName(u"tableView")

        self.table_item = QStandardItemModel(0, 3, self)
        self.table_item.setHorizontalHeaderLabels(['时间', '模块', '操作'])
        self.tableView.setModel(self.table_item)
        self.tableView.setColumnWidth(0, 100)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButton_3 = QToolButton(self)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout.addWidget(self.toolButton_3)

        self.toolButton_2 = QToolButton(self)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout.addWidget(self.toolButton_2)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslate()

        QMetaObject.connectSlotsByName(self)

    def retranslate(self):
        self.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.toolButton_3.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa", None))
        self.toolButton_2.setText(QCoreApplication.translate("Form", u"\u8fc7\u6ee4", None))

    @Slot()
    def update_log(self, log_info):

        self.table_item.setItem(self.buffer_size, 0, QStandardItem(log_info['tm']))
        self.table_item.setItem(self.buffer_size, 1, QStandardItem(log_info['module']))
        self.table_item.setItem(self.buffer_size, 2, QStandardItem(log_info['msg']))
        self.buffer_size += 1
