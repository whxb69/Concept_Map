# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'find.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

class Find_Form(object):
    def setupUi(self):
        self.line_find = QtWidgets.QLineEdit(self)
        self.line_find.setGeometry(QtCore.QRect(90, 30, 281, 41))
        self.line_find.setObjectName("line_find")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 61, 24))
        self.label_2.setObjectName("label_2")
        self.btn_next = QtWidgets.QPushButton(self)
        self.btn_next.setGeometry(QtCore.QRect(480, 30, 150, 46))
        self.btn_next.setObjectName("btn_next")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 40, 61, 24))
        self.label.setObjectName("label")
        self.btn_replace = QtWidgets.QPushButton(self)
        self.btn_replace.setGeometry(QtCore.QRect(480, 160, 150, 46))
        self.btn_replace.setObjectName("btn_replace")
        self.btn_reall = QtWidgets.QPushButton(self)
        self.btn_reall.setGeometry(QtCore.QRect(480, 230, 150, 46))
        self.btn_reall.setObjectName("btn_reall")
        self.line_find_2 = QtWidgets.QLineEdit(self)
        self.line_find_2.setGeometry(QtCore.QRect(90, 90, 281, 41))
        self.line_find_2.setObjectName("line_find_2")
        self.btn_prev = QtWidgets.QPushButton(self)
        self.btn_prev.setGeometry(QtCore.QRect(480, 100, 150, 46))
        self.btn_prev.setObjectName("btn_prev")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(30, 170, 351, 121))
        self.groupBox.setObjectName("groupBox")
        self.get_sel = QtWidgets.QRadioButton(self.groupBox)
        self.get_sel.setGeometry(QtCore.QRect(20, 50, 141, 28))
        self.get_sel.setObjectName("get_sel")
        self.get_all = QtWidgets.QRadioButton(self.groupBox)
        self.get_all.setGeometry(QtCore.QRect(210, 50, 91, 28))
        self.get_all.setObjectName("get_all")

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.label_2.setText(_translate("self", "替换:"))
        self.btn_next.setText(_translate("self", "下一个"))
        self.label.setText(_translate("self", "查找:"))
        self.btn_replace.setText(_translate("self", "替换"))
        self.btn_reall.setText(_translate("self", "替换全部"))
        self.btn_prev.setText(_translate("self", "上一个"))
        self.groupBox.setTitle(_translate("self", "区域选择"))
        self.get_sel.setText(_translate("self", "选中区域"))
        self.get_all.setText(_translate("self", "全部"))
        # QtCore.QMetaObject.connectSlotsByName(self)



