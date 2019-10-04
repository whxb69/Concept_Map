from ui import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cgitb
import math

cgitb.enable()


class Newlable(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(None, parent)
        self.state = None
        self.setText('New Note')
        self.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                           "border-color: rgb(240,240,240);background-color:rgb(240,240,240)")
        self.setAcceptDrops(False)
        self.setReadOnly(True)
        self.setDisabled(False)
        self.mm = False  # move mode
        self.press = False
        self.tgt = None
        self.draw = False

    def mouseDoubleClickEvent(self, event):
        self.setReadOnly(False)
        self.setStyleSheet("border-width:2px;border-style: solid; "
                           "border-radius: 15px;border-color: rgb(150, 100, 0);")

    def mousePressEvent(self, QMouseEvent):
        self.press = True

    def mouseMoveEvent(self, event):
        if self.press:
            self.mm = True
            if not hasattr(self, 'temp'):
                self.temp = win.inittag(self.x()+90, self.y()+90)
                self.temp.setObjectName(self.objectName())
                self.setObjectName('temp')
                self.setStyleSheet("border-style:none;background-color:rgb(240,240,240)")

            # if isinstance(temp,Newlable):
            wx = win.x()
            wy = win.y()
            x = event.globalX()
            y = event.globalY()
            self.move(x - wx - 90, y - wy - 90)

            alltag = win.findChildren(QLineEdit)
            for tag in alltag:
                tx = tag.x()
                ty = tag.y()
                distance = math.sqrt((self.x() - tx) ** 2 + (self.y() - ty) ** 2)
                if distance <= 80.7:
                    if tag not in [self.temp, self]:
                        tag.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                                          "border-color: rgb(0, 0, 0);background-color: gray;")
                        self.tgt = tag
                else:
                    tag.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                                      "border-color: rgb(0, 0, 0);")
                    if self.tgt == tag:
                        self.tgt = None

    def mouseReleaseEvent(self, event):
        self.press = False
        if self.state == 'select':
            self.setReadOnly(False)
            self.setStyleSheet("border-width:2px;border-style: solid; "
                               "border-radius: 15px;border-color: rgb(150, 100, 0);")
            print(self.acceptDrops())

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

        if self.mm:
            self.draw = True
            wx = win.x()
            wy = win.y()
            x = event.globalX()
            y = event.globalY()
            if self.tgt:
                win.drawline_pt(self.temp, self.tgt)
            else:
                self.temp.move(x - wx - 90, y - wy - 90)
                win.update()
                self.tgt = None
                self.mm = False
            self.deleteLater()

    def enterEvent(self, event):
        if self.state != 'select':
            self.state = 'in'
            self.setStyleSheet("border-width:1.5px;border-style: dashed; "
                               "border-radius: 15px;border-color: rgb(0, 0, 0);"
                               "background-color: (240,240,240)")

    def leaveEvent(self, event):
        if self.state != 'select':
            self.state = None
            self.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                               "border-color: rgb(0, 0, 0);background-color: (240,240,240)")

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setupUi(self)
        # self.lines = []
        self.lines = {}
        self.draw = False
        self.lpos = (None, None)

    def paintEvent(self, event):
        if self.draw and hasattr(self, 'lines'):
            pen = QPainter(self)
            pen.begin(self)
            for s in self.lines:
                for l in self.lines[s]:
                    ss = win.findChild(QLineEdit, s)
                    ee = win.findChild(QLineEdit, l)
                    line = QLineF(ss.x() + 90, ss.y() + 30, ee.x() + 90, ee.y() + 30)
                    line.setLength(line.length())
                    pen.setPen(QPen(Qt.darkRed, 2, Qt.DashLine))
                    pen.drawLine(line)
                    self.drawarrow(pen, line)
            pen.end()

    def drawarrow(self, pen, line):
        v = line.unitVector()
        v.setLength(20)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(line.dx()/2, line.dy()/2))

        n = v.normalVector()  # 法向量
        n.setLength(n.length() * 0.5)  # 这里设定箭头的宽度

        n2 = n.normalVector().normalVector()

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()

        pen.setPen(QPen(Qt.darkRed, 2, Qt.SolidLine))
        pen.drawPolygon(p1, p2, p3)

    def drawline_pt(self, s, e):
        self.draw = True
        if s.objectName() not in self.lines:
            self.lines[s.objectName()] = [e.objectName()]
        else:
            if e.objectName() in self.lines[s.objectName()]:
                self.lines[s.objectName()].remove(e.objectName())
            else:
                self.lines[s.objectName()].append(e.objectName())
        self.update()

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
        
        self.inittag(x - wx, y - wy)

    def inittag(self, x, y):
        alltag = self.findChildren(QLineEdit)
        print([tag.objectName() for tag in alltag])
        name = 'tag' + str(len(alltag)+1)
        exec('self.%s = Newlable(self)' % name)
        exec('self.%s.setGeometry(x - 90, y - 90, 180, 60)' % name)
        exec('self.%s.show()' % name)
        exec('self.%s.setObjectName("%s")' % (name, name))

        return eval('self.%s'%name)

    def modify_txt(self):
        self.tag1.setTextInteractionFlags(Qt.TextEditorInteraction)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Mainwindow()
    win.show()
    sys.exit(app.exec_())
