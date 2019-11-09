# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QLabel, QScrollArea, QScrollBar, QHBoxLayout


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(r'src\concept.png'))
        desktop = QtWidgets.QApplication.desktop()
        self.screenWidth = desktop.width() * 0.7
        self.screenHeight = desktop.height() * 0.6
        MainWindow.resize(self.screenWidth , self.screenHeight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.centralwidget.setMouseTracking(True)
        self.hbox = QHBoxLayout()
        self.centralwidget.setLayout(self.hbox)


        # self.sb = QScrollBar(self)
        # # self.sb.setMinimum(0.5*self.screenHeight)
        # MainWindow.layout()
        # self.hbox.addWidget(self.sb)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1941, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.logo = QLabel(self)
        self.logo.setText('双击任意位置创建标签\n'
                          '文本拖动到两侧可生成标签\n'
                          '拖动标签相互接触创建连接')
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.resize(self.screenWidth/5,self.screenHeight/8)
        self.logo.move(self.screenWidth*0.4,self.screenHeight*7/16)

        self.action_new = QAction("&新建", MainWindow)
        self.action_new.setObjectName("actionnew")
        self.action_new.setToolTip('新建窗口')

        self.action_open = QAction("&打开", MainWindow)
        self.action_open.setObjectName("actionopen")
        self.action_open.setToolTip('打开文件')

        self.action_save = QAction("&保存", MainWindow)
        self.action_save.setObjectName("actionsave")
        self.action_save.setToolTip('保存文件')

        self.action_saveas = QAction("&另存为", MainWindow)
        self.action_saveas.setObjectName("actionsaveas")
        self.action_saveas.setToolTip('另存为文件')

        m_file = self.menubar.addMenu('文件')
        m_file.addAction(self.action_new)#新建
        m_file.addAction(self.action_open)#打开
        m_file.addAction(self.action_save)#保存
        m_file.addAction(self.action_saveas)#另存为

        self.action_undo = QAction("&撤销", MainWindow)
        self.action_undo.setObjectName("actionundo")
        self.action_undo.setToolTip('撤销')

        self.action_cut = QAction("&剪切", MainWindow)
        self.action_cut.setObjectName("actioncut")
        self.action_cut.setToolTip('剪切')

        self.action_copy = QAction("&复制", MainWindow)
        self.action_copy.setObjectName("actioncopy")
        self.action_copy.setToolTip('复制')

        self.action_paste = QAction("&粘贴", MainWindow)
        self.action_paste.setObjectName("actionpaste")
        self.action_paste.setToolTip('粘贴')

        self.action_delete = QAction("&删除", MainWindow)
        self.action_delete.setObjectName("actionsave")
        self.action_delete.setToolTip('删除')

        self.action_find = QAction("&查找", MainWindow)
        self.action_find.setObjectName("actionsave")
        self.action_find.setToolTip('查找')

        self.action_selectall = QAction("&全选", MainWindow)
        self.action_selectall.setObjectName("actionselectall")
        self.action_selectall.setToolTip('全选')

        m_edit = self.menubar.addMenu('编辑')
        m_edit.addAction(self.action_undo) # 撤销
        m_edit.addSeparator()
        m_edit.addAction(self.action_cut)  # 剪切
        m_edit.addAction(self.action_copy)  # 复制
        m_edit.addAction(self.action_paste)  # 粘贴
        m_edit.addSeparator()
        m_edit.addAction(self.action_delete)  # 删除
        m_edit.addAction(self.action_find)  # 查找
        m_edit.addAction(self.action_selectall)  # 全选

        self.action_newtag = QAction("&新建标签", MainWindow)
        self.action_newtag.setObjectName("actionnewtag")
        self.action_newtag.setToolTip('新建')

        self.action_newtags= QAction("&批量新建", MainWindow)
        self.action_newtags.setObjectName("actionnewtags")
        self.action_newtags.setToolTip('批量新建')

        m_note = self.menubar.addMenu('标签')
        m_note.addAction(self.action_newtag)
        m_note.addAction(self.action_newtags)




        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
