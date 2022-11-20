
from PySide6.QtCore import (QMetaObject, QCoreApplication)
from PySide6.QtWidgets import (QSizePolicy, QHBoxLayout, QVBoxLayout,
                               QToolButton, QTableView, QSpacerItem)


class LogViewer:

    def setup(self, Form):
        print("初始化日志显示器···")
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        Form.setMaximumHeight(300)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = QTableView(Form)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButton_3 = QToolButton(Form)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout.addWidget(self.toolButton_3)

        self.toolButton_2 = QToolButton(Form)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout.addWidget(self.toolButton_2)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslate(Form)

        QMetaObject.connectSlotsByName(Form)

    def retranslate(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.toolButton_3.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa", None))
        self.toolButton_2.setText(QCoreApplication.translate("Form", u"\u8fc7\u6ee4", None))
