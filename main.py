from ui import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cgitb
import math

cgitb.enable()


class Newlable(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(None, parent)
        # self.poslog = []
        self.state = None
        self.setText('New Note')
        self.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                           "border-color: rgb(0, 0, 0);")
        self.setAcceptDrops(False)
        self.setReadOnly(True)
        self.setDisabled(False)
        self.mm = False  # move mode
        self.press = False

    def mouseDoubleClickEvent(self, event):
        # print('yes')
        # self.setAcceptDrops(True)
        self.setReadOnly(False)
        self.setStyleSheet("border-width:2px;border-style: solid; "
                           "border-radius: 15px;border-color: rgb(150, 100, 0);")

    def mousePressEvent(self, QMouseEvent):
        self.press = True

    def mouseMoveEvent(self, QMouseEvent):
        # print(self.press)
        # if self.state in ['in', 'select']:
        if self.press:
            if not self.mm:
                self.mm = True
                self.focusNextChild()
                self.label = templabel(self, self.x(), self.y(), win)
                self.label.show()
                self.label.setFocus()
                print(self.label.hasFocus())
            else:
                x = self.label.x()
                y = self.label.y()
                self.label.move(x, y)

    def mouseReleaseEvent(self, QMouseEvent):
        self.press = False
        if self.state == 'select':
            self.setReadOnly(False)
            self.setStyleSheet("border-width:2px;border-style: solid; "
                               "border-radius: 15px;border-color: rgb(150, 100, 0);")
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
        self.state = None
        self.setText(match.text())
        self.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                           "border-color: rgb(0, 0, 0);")
        # self.setAcceptDrops(False)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setGeometry(x, y, 150, 60)
        self.match = match
        self.mm = False
        self.tgt = None
        self.draw = False
        self.press = True

        # self.setFocus()

    def getline(self, tagname):
        tgt = win.findChild(QLineEdit, tagname)
        if tgt != self.match:
            tgt.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                              "border-color: rgb(0, 0, 0);background-color: gray;")
            print(tgt)

    def mouseMoveEvent(self, event):
        if self.press:
            if not self.mm:
                self.mm = True
            wx = win.x()
            wy = win.y()
            x = event.globalX()
            y = event.globalY()
            self.move(x - wx - 75, y - wy - 90)

            alltag = win.findChildren(QLineEdit)
            for tag in alltag:
                tx = tag.x()
                ty = tag.y()
                distance = math.sqrt((self.x() - tx) ** 2 + (self.y() - ty) ** 2)
                if distance <= 80.7:
                    if tag != self.match:
                        tag.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                                          "border-color: rgb(0, 0, 0);background-color: gray;")
                        self.tgt = tag
                else:
                    tag.setStyleSheet("border-width: 0px;border-radius: 15px; border-style: solid;"
                                      "border-color: rgb(0, 0, 0);")
                    if self.tgt == tag:
                        self.tgt = None

    def mousePressEvent(self, QMouseEvent):
        self.press = True

    def mouseReleaseEvent(self, QMouseEvent):
        self.match.mm = False
        self.mm = False
        wx = win.x()
        wy = win.y()
        x = QMouseEvent.globalX()
        y = QMouseEvent.globalY()
        print(self.tgt)
        if self.tgt:
            self.draw = True
            # win.drawline(self.tgt.x() + 75, self.tgt.y() + 30,
                         # self.match.x() + 75, self.match.y() + 30)
            win.drawline_pt(self.match,self.tgt)
        else:
            self.match.move(x - wx - 75, y - wy - 90)
        self.deleteLater()
        win.update()
        # self.l_fun.quit()


# class Line(QThread):
#     get = pyqtSignal(str)
#
#     def __init__(self,label, parent=None):
#         super(Line,self).__init__(parent)
#         self.label = label
#         self.lx = label.x()
#         self.ly = label.y()
#
#     def __del__(self):
#         self.wait()
#
#     def run(self):
#         while self.label.mm:
#             # print(1)
#             alltag = win.findChildren(QLineEdit)
#             print(len(alltag))
#             for tag in alltag:
#                 tx = tag.x()
#                 ty = tag.y()
#                 distance = math.sqrt((self.lx-tx)**2+(self.ly-ty)**2)
#                 # print(distance)
#                 if distance <= 78.8:
#                     print(self.lx,tx,self.ly,ty)
#                     self.get.emit(tag.objectName())
#                     #
#                     # return tag

# def stop(self):
#     self.trigger.emit()

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setupUi(self)
        # self.lines = []
        self.lines = {}
        self.draw = False

    def paintEvent(self, event):
        # if self.draw:
        if hasattr(self,'lines'):
            pen = QPainter(self)
            pen.begin(self)
            for s in self.lines:
                for l in self.lines[s]:
                    print(s,l)
                    ss = win.findChild(QLineEdit, s)
                    ee = win.findChild(QLineEdit, l)
                    line = QLineF(ss.x()+75, ss.y()+30, ee.x()+75, ee.y()+30)
                    line.setLength(line.length() - 70)
                    pen.setPen(QPen(Qt.darkRed, 2, Qt.DashLine))
                    pen.drawLine(line)
                    self.drawarrow(pen, line)
                # TODO:计算直线具体减少长度
            pen.end()

    def drawarrow(self, pen, line):
        v = line.unitVector()
        v.setLength(20)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(line.dx(), line.dy()))
        n = v.normalVector()  # 法向量
        n.setLength(n.length() * 0.5)  # 这里设定箭头的宽度
        n2 = n.normalVector().normalVector()
        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        pen.setPen(QPen(Qt.darkRed, 2, Qt.SolidLine))
        pen.drawPolygon(p1, p2, p3)

    def drawline(self, tx, ty, mx, my):
        self.Line_list = [mx, my, tx, ty]
        self.lines.append([mx, my, tx, ty])
        self.update()

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
        self.draw = False

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
