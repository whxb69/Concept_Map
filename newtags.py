# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newtags.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class New_Form(object):
    def setupUi(self, app):
        self.setObjectName("Form")
        self.resize(445, 207)
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setGeometry(QtCore.QRect(130, 50, 166, 30))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setObjectName("label")
        self.spinBox = QtWidgets.QSpinBox(self.splitter)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(2)
        self.spinBox.setMaximum(10)
        self.splitter_2 = QtWidgets.QSplitter(self)
        self.splitter_2.setGeometry(QtCore.QRect(60, 110, 300, 46))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.btn_yes = QtWidgets.QPushButton(self.splitter_2)
        self.btn_yes.setObjectName("btn_yes")
        self.btn_no = QtWidgets.QPushButton(self.splitter_2)
        self.btn_no.setObjectName("btn_no")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "新建个数"))
        self.btn_yes.setText(_translate("Form", "新建"))
        self.btn_no.setText(_translate("Form", "取消"))

