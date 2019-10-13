# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QLabel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(r'src\concept.png'))
        desktop = QtWidgets.QApplication.desktop()
        self.screenWidth = desktop.width() * 0.5
        self.screenHeight = desktop.height() * 0.7
        MainWindow.resize(self.screenWidth , self.screenHeight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.centralwidget.setMouseTracking(True)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1941, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_new = QAction("&新建", MainWindow)
        self.action_new.setObjectName("actionnew")
        self.action_new.setToolTip('新建窗口')

        self.action_open = QAction("&打开", MainWindow)
        self.action_open.setObjectName("actionopen")
        self.action_open.setToolTip('打开文件')

        self.action_save = QAction("&保存", MainWindow)
        self.action_save.setObjectName("actionsave")
        self.action_save.setToolTip('保存文件')

        self.action_copy = QAction("&另存为", MainWindow)
        self.action_copy.setObjectName("actionsave")
        self.action_copy.setToolTip('另存为文件')

        file = self.menubar.addMenu('文件')
        file.addAction(self.action_new)
        file.addAction(self.action_open)
        file.addAction(self.action_save)
        file.addAction(self.action_copy)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
