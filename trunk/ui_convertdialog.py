# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/zoomtc/convertdialog.ui'
#
# Created: Tue Aug 31 22:43:35 2010
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_convertDialog(object):
    def setupUi(self, convertDialog):
        convertDialog.setObjectName("convertDialog")
        convertDialog.setWindowModality(QtCore.Qt.WindowModal)
        convertDialog.resize(419,126)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.jpg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        convertDialog.setWindowIcon(icon)
        convertDialog.setModal(False)
        self.gridLayout_2 = QtGui.QGridLayout(convertDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.dirLabel = QtGui.QLabel(convertDialog)
        self.dirLabel.setObjectName("dirLabel")
        self.gridLayout.addWidget(self.dirLabel,0,0,1,1)
        self.dirLineEdit = QtGui.QLineEdit(convertDialog)
        self.dirLineEdit.setObjectName("dirLineEdit")
        self.gridLayout.addWidget(self.dirLineEdit,0,1,1,1)
        self.dirButton = QtGui.QPushButton(convertDialog)
        self.dirButton.setObjectName("dirButton")
        self.gridLayout.addWidget(self.dirButton,0,2,1,1)
        self.rateLabel = QtGui.QLabel(convertDialog)
        self.rateLabel.setObjectName("rateLabel")
        self.gridLayout.addWidget(self.rateLabel,1,0,1,1)
        self.rateLineEdit = QtGui.QLineEdit(convertDialog)
        self.rateLineEdit.setObjectName("rateLineEdit")
        self.gridLayout.addWidget(self.rateLineEdit,1,1,1,1)
        self.convertButton = QtGui.QPushButton(convertDialog)
        self.convertButton.setObjectName("convertButton")
        self.gridLayout.addWidget(self.convertButton,1,2,1,1)
        self.gridLayout_2.addLayout(self.gridLayout,0,0,1,1)
        self.helpLabel = QtGui.QLabel(convertDialog)
        self.helpLabel.setObjectName("helpLabel")
        self.gridLayout_2.addWidget(self.helpLabel,1,0,1,1)

        self.retranslateUi(convertDialog)
        QtCore.QMetaObject.connectSlotsByName(convertDialog)

    def retranslateUi(self, convertDialog):
        convertDialog.setWindowTitle(QtGui.QApplication.translate("convertDialog", "执法督查科图片批量处理工具", None, QtGui.QApplication.UnicodeUTF8))
        self.dirLabel.setText(QtGui.QApplication.translate("convertDialog", "图片源目录：", None, QtGui.QApplication.UnicodeUTF8))
        self.dirButton.setText(QtGui.QApplication.translate("convertDialog", "浏览", None, QtGui.QApplication.UnicodeUTF8))
        self.rateLabel.setText(QtGui.QApplication.translate("convertDialog", "转换比例：", None, QtGui.QApplication.UnicodeUTF8))
        self.convertButton.setText(QtGui.QApplication.translate("convertDialog", "转换", None, QtGui.QApplication.UnicodeUTF8))
        self.helpLabel.setText(QtGui.QApplication.translate("convertDialog", "1.\n"
"2\n"
"3", None, QtGui.QApplication.UnicodeUTF8))

import zoomtc_rc
