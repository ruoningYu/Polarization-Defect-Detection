# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (
    QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout)


class About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(453, 211)
        self.verticalLayout = QVBoxLayout(About)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QTextBrowser(About)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.AboutOK = QPushButton(About)
        self.AboutOK.setObjectName(u"AboutOK")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.AboutOK.sizePolicy().hasHeightForWidth())
        self.AboutOK.setSizePolicy(sizePolicy)
        self.AboutOK.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout.addWidget(self.AboutOK)

        self.retranslateUi(About)
        self.AboutOK.clicked.connect(About.close)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(
            QCoreApplication.translate("About", u"ABOUT", None))
        self.textBrowser.setHtml(QCoreApplication.translate(
            "About", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:16pt; font-weight:600;\">\u7f3a\u9677\u68c0\u6d4b\u7cfb\u7edf</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:10pt; font-weight:600;\">Version 1.0.0</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:10pt;\">\u672c\u8f6f\u4ef6\u57fa\u4e8e\u504f\u632f\u56fe\u50cf\u53ca\u6df1\u5ea6\u5b66\u4e60\u5bf9\u5de5\u4e1a\u4ef6\u8fdb\u884c"
            "\u7f3a\u9677\u68c0\u6d4b</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:10pt;\">\u672c\u8f6f\u4ef6\u57fa\u4e8eOpencv\u53ca\u5176\u4ed6\u5f00\u6e90\u9879\u76ee\u6784\u5efa</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:10pt;\">\u672c\u8f6f\u4ef6\u9075\u5faaApache Licence 2.0\u5f00\u6e90\u534f\u8bae</span></p></body></html>", None))
        self.AboutOK.setText(QCoreApplication.translate("About", u"OK", None))
    # retranslateUi
