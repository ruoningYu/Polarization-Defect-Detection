
from PySide6.QtCore import (QMetaObject, QCoreApplication)
from PySide6.QtWidgets import (QSizePolicy, QHBoxLayout, QVBoxLayout,
                               QToolButton, QTableView, QSpacerItem,
                               QWidget)


class LogViewer(QWidget):

    def __init__(self, parent):
        super(LogViewer, self).__init__(parent)
        print("初始化日志显示器···")

        self.setObjectName(u"Form")
        self.resize(400, 300)
        self.setMaximumHeight(300)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = QTableView(self)
        self.tableView.setObjectName(u"tableView")

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
