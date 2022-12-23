# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (
    QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout)


class Help(object):
    def setupUi(self, Help):
        if not Help.objectName():
            Help.setObjectName(u"Help")
        Help.resize(514, 435)
        self.verticalLayout = QVBoxLayout(Help)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.HelpDoc = QTextBrowser(Help)
        self.HelpDoc.setObjectName(u"HelpDoc")

        self.verticalLayout.addWidget(self.HelpDoc)

        self.retranslateUi(Help)

        QMetaObject.connectSlotsByName(Help)
    # setupUi

    def retranslateUi(self, Help):
        Help.setWindowTitle(QCoreApplication.translate("Help", u"Help", None))
    # retranslateUi
