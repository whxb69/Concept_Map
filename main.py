from ui import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QMouseEvent
import cgitb


cgitb.enable()


class Newlable(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(None, parent)
        self.poslog = []
        self.state = None
        self.setText('New Note')
        self.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                           "border-color: rgb(0, 0, 0);")
        self.setAcceptDrops(False)
        self.setReadOnly(True)
        self.setDisabled(False)
        self.mm = False
        self.press = False

    def mouseDoubleClickEvent(self, event):
        print('yes')
        # self.setAcceptDrops(True)
        self.setReadOnly(False)

    def mousePressEvent(self, QMouseEvent):
        self.press = True

    def mouseMoveEvent(self, QMouseEvent):
        print(self.press)
        if self.state in ['in', 'select']:
            if self.press and not self.mm:
                self.mm = True
                label = templabel(self, self.x(), self.y(), win)
                print(label.hasFocus())
                label.setFocus(True)
                print(label.hasFocus())
                label.show()

    def mouseReleaseEvent(self, QMouseEvent):
        self.press = False
        if self.state == 'select':
            self.setReadOnly(False)
            # self.setAcceptDrops(True)
            print(self.acceptDrops())
            # label = templabel(self.text(), self.x(), self.y(), win)
            # label.show()
            # self.state = 'move'
        elif self.state == 'in':
            alltag = win.findChildren(QLineEdit)
            for tag in alltag:
                if tag.state == 'select':
                    tag.state = None
                    tag.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                                      "border-color: rgb(0, 0, 0);")
                    break
            self.state = 'select'
            self.setStyleSheet("border-width:3px;border-style: solid; "
                               "border-radius: 15px;border-color: rgb(150, 100, 0);")

    def enterEvent(self, event):
        if self.state != 'select':
            self.state = 'in'
            self.setStyleSheet("border-width:1.5px;border-style: dashed; "
                               "border-radius: 15px;border-color: rgb(0, 0, 0);")

    def leaveEvent(self, event):
        if self.state != 'select':
            self.state = None
            self.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                               "border-color: rgb(0, 0, 0);")


class templabel(QLabel):
    def __init__(self, match, x, y, parent=None):
        super().__init__(None, parent)
        self.poslog = []
        self.state = None
        self.setText(match.text())
        self.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                           "border-color: rgb(0, 0, 0);")
        # self.setAcceptDrops(False)
        self.setGeometry(x, y, 150, 60)
        self.match = match

    def mouseMoveEvent(self, event):
        # if win.label1.state == 'move':
        print('press')
        wx = win.x()
        wy = win.y()
        x = event.globalX()
        y = event.globalY()
        self.poslog.append([x - wx - 90, y - wy - 90])
        self.move(x - wx - 90, y - wy - 90)

    def mousePressEvent(self, QMouseEvent):
        print('press')

    def mouseReleaseEvent(self, QMouseEvent):
        self.match.mm= False
        wx = win.x()
        wy = win.y()
        x = QMouseEvent.globalX()
        y = QMouseEvent.globalY()
        self.match.move(x - wx - 90, y - wy - 90)
        self.deleteLater()


class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setupUi(self)

    def mousePressEvent(self, event):
        alltag = self.findChildren(QLineEdit)
        for tag in alltag:
            if tag.state:
                tag.setReadOnly(True)
                tag.setSelection(0, 0)
                tag.state = None
                tag.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                                  "border-color: rgb(0, 0, 0);")
                break

    def mouseDoubleClickEvent(self, event):
        wx = self.x()
        wy = self.y()
        x = event.globalX()
        y = event.globalY()
        alltag = self.findChildren(QLineEdit)
        print([tag.objectName() for tag in alltag])
        self.inittag(len(alltag) + 1, x - wx, y - wy)
        print(2)

    def inittag(self, no, x, y):
        name = 'tag' + str(no)
        exec('self.%s = Newlable(self)' % name)
        exec('self.%s.setGeometry(x - 90, y - 90, 180, 60)' % name)
        exec('self.%s.show()' % name)
        exec('self.%s.setObjectName("%s")' % (name, name))

    def modify_txt(self):
        self.tag1.setTextInteractionFlags(Qt.TextEditorInteraction)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Mainwindow()
    win.show()
    sys.exit(app.exec_())
