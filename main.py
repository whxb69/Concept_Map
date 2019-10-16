from ui import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cgitb
import math
from xml.etree import ElementTree as ET
import time
import os
import PyQt5.sip

cgitb.enable()


class Newlable(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(None, parent)
        self.textChanged.connect(self.widthchange)
        self.state = 'edit'
        self.setText('New Note')
        self.sheet = {'None': "border-width:0px;border-style: None; "
                              "border-radius: 15px;background-color:rgb(240,240,240)",
                      'edit': "border-width:2px;border-style: solid; "
                              "border-radius: 15px;border-color: rgb(150, 100, 0);",
                      'in': "border-width:1.5px;border-style: dashed; "
                            "border-radius: 15px;border-color: rgb(0, 0, 0);"
                            "background-color:rgb(240,240,240)",
                      'B': "border-width:5px;border-style: solid; "
                           "border-radius: 15px;border-color: rgb(0, 0, 0);"
                           "background-color:rgb(240,240,240)",
                      'select': "border-width:3px;border-style: solid; "
                                "border-radius: 15px;border-color: rgb(150, 100, 0);",
                      'crash': "border-width: 0px;border-radius: 15px; border-style: solid;"
                               "border-color: rgb(0, 0, 0);background-color: gray;",
                      'Bcrash': "border-width: 5px;border-radius: 15px; border-style: solid;"
                                "border-color: rgb(0, 0, 0);background-color: gray;",
                      'move': "border-width:0px;border-radius: 15px;"
                              "border-color: rgb(0, 0, 0);background-color:rgb(240,240,240)"}
        self.setStyleSheet(self.sheet['edit'])
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setReadOnly(False)
        self.setSelection(0, len(self.text()))
        # self.setFocus()
        self.setAlignment(Qt.AlignCenter)
        self.mm = False  # move mode
        self.press = False
        self.tgt = None
        self.draw = False
        self.Bstate = False


        self.opos = None

        self.window = self.parentWidget()
        # TODO:修改时不能点光标
        # TODO:edit状态下无法托选
        # TODO:B框和select与edit的结合
        # TODO:连线后B状态消失 估计问题在temp

    def widthchange(self):
        length = self.fontMetrics().width(self.text())
        s_size = length/len(self.text())
        if length>=self.width()-2*s_size:
            self.resize(length+2*s_size,self.height())

    def changeEvnet(self, evnet):
        self.window.changed = True

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        Bcase = menu.addAction("&Bcase")
        Bcase.triggered.connect(self.B_fun)
        menu.exec_(event.globalPos())

    def mouseDoubleClickEvent(self, event):
        self.state = 'edit'
        self.setReadOnly(False)
        self.setAcceptDrops(True)
        self.setFocus()

        alltag = self.window.findChildren(QLineEdit)
        for tag in alltag:
            if tag != self:
                tag.state = None
            if not tag.Bstate:
                tag.setStyleSheet(tag.sheet['None'])

        self.setStyleSheet(self.sheet[self.state])

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if self.state == 'select':
                name = self.objectName()
                if name in self.window.lines:
                    self.window.lines.pop(name)
                for k in self.window.lines:
                    if name in self.window.lines[k]:
                        self.window.lines[k].remove(name)
                self.window.update()

                self.deltag()
        else:
            self.window.keyPressEvent(event)

    def mousePressEvent(self, event):
        if self.state != 'edit':
            self.press = True
        else:
            event.ignore()
            # TODO:全局判断鼠标位置 实现光标可点

    def moveEvent(self, event):
        if not self.opos:
            self.opos = event.pos()
        if self.window.selects:
            pass

    def mouseMoveEvent(self, event):
        if self.press and self.state != 'edit':
            self.mm = True
            if not hasattr(self, 'temp'):
                # 触发位移时定义占位tag
                self.temp = self.window.inittag(self.x() + 90, self.y() + 90)
                self.temp.setObjectName(self.objectName())
                self.temp.setText(self.text())
                self.temp.setReadOnly(True)
                self.temp.setAcceptDrops(False)
                if self.Bstate:
                    self.temp.setStyleSheet(self.sheet['B'])
                    self.temp.Bstate = True
                else:
                    self.temp.setStyleSheet('None')
                self.setObjectName('temp')
                self.setStyleSheet(self.sheet['move'])

            wx = self.window.x()
            wy = self.window.y()
            x = event.globalX()
            y = event.globalY()
            self.move(x - wx - 90, y - wy - 90)

            alltag = self.window.findChildren(QLineEdit)
            for tag in alltag:
                tx = tag.x()
                ty = tag.y()
                rect = QRect(QPoint(tx,ty),QPoint(tx+tag.width(),ty+tag.height()))
                point = QPoint(event.globalX()-self.window.x(),
                event.globalY()-self.window.y()-tag.height())
                if rect.contains(point):
                    if tag not in [self.temp, self]:
                        if tag.Bstate:
                            tag.setStyleSheet(tag.sheet['Bcrash'])
                        else:
                            tag.setStyleSheet(tag.sheet['crash'])
                        self.tgt = tag
                    else:
                        tag.setStyleSheet(tag.sheet['None'])
                else:
                    if tag.Bstate:
                        tag.setStyleSheet(tag.sheet['B'])
                    else:
                        tag.setStyleSheet(tag.sheet['None'])
                    if self.tgt == tag:
                        self.tgt = None

    def mouseReleaseEvent(self, event):
        self.press = False
        if self.state == 'select':
            self.state = 'edit'
            self.setReadOnly(False)
            self.setAcceptDrops(True)
            self.setFocus()
            self.setStyleSheet(self.sheet[self.state])

        elif self.state == 'in':
            alltag = self.window.findChildren(QLineEdit)
            for tag in alltag:
                if tag.state in ['select', 'edit']:
                    tag.state = None
                    tag.setStyleSheet(self.sheet['None'])
                    break
            self.setStyleSheet(self.sheet['select'])
            self.state = 'select'

        #release结束移动
        if self.mm:
            self.draw = True
            wx = self.window.x()
            wy = self.window.y()
            x = event.globalX()
            y = event.globalY()
            if self.tgt:
                #连接后画线
                self.window.drawline_pt(self.temp, self.tgt)
                if self.tgt.Bstate:
                    self.tgt.setStyleSheet(self.temp.sheet['B'])
                else:
                    self.tgt.setStyleSheet(self.tgt.sheet['None'])
            else:
                #非连接 移动tag
                self.temp.move(x - wx - 90, y - wy - 90)
                self.tgt = None
                self.mm = False
            self.temp.setReadOnly(True)
            self.temp.state = None
            if self.temp.Bstate:
                self.temp.setStyleSheet(self.temp.sheet['B'])
            self.window.update()
            self.deltag()

    def enterEvent(self, event):
        if self.state not in ['select', 'edit']:
            self.state = 'in'
            if not self.Bstate:
                self.setStyleSheet(self.sheet[self.state])
            else:
                self.setStyleSheet(self.sheet['B'])

    def leaveEvent(self, event):
        if self.state not in ['select', 'edit']:
            self.state = None
            if not self.Bstate:
                self.setStyleSheet(self.sheet['None'])
            else:
                self.setStyleSheet(self.sheet['B'])

    def B_fun(self):
        self.Bstate = True
        self.setStyleSheet(self.sheet['B'])

    def deltag(self):
        keys = []  # 待删除arrows索引
        if self.window.arrows:
            for key, value in self.window.arrows.items():
                if self in value:
                    keys.append(key)
        [self.window.arrows.pop(key) for key in keys]
        self.deleteLater()


class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setupUi(self)
        # self.lines = []
        self.setWindowTitle("Concept map")
        self.lines = {}
        self.draw = False
        self.lpos = (None, None)
        self.arrows = {}
        self.load = False
        self.arrows_num = 1
        self.num = 1
        self.setMouseTracking(True)
        self.nodes = {}
        self.window = self
        self.press = False
        self.filename = None
        self.changed = False
        self.setAcceptDrops(True)
        self.press_s = None
        self.selects = []

        self.action_save.triggered.connect(lambda: self.savefile(self.filename))
        self.action_copy.triggered.connect(self.saveasfile)
        self.action_open.triggered.connect(self.openfile)
        self.action_new.triggered.connect(self.newfile)

        self.label_tag = Dlabel(self)
        self.label_tag.setObjectName('tag')
        self.label_tag.setGeometry(
            QtCore.QRect(0, 0.25 * self.screenHeight, 20, 0.5 * self.screenHeight))

        self.label_rel = Dlabel(self)
        self.label_rel.setObjectName('rel')
        self.label_rel.setGeometry(
            QtCore.QRect(self.screenWidth - 20, 0.25 * self.screenHeight, 20,
                         0.5 * self.screenHeight))

    def resizeEvent(self, event):
        # 保持Dlabel相对方位和大小
        self.label_tag.resize(20, 0.5 * self.height())
        self.label_tag.move(0, 0.25 * self.height())
        self.label_rel.resize(20, 0.5 * self.height())
        self.label_rel.move(self.width() - 20, 0.25 * self.height())

    def closeEvent(self, event):
        # 画布有变动
        if self.changed:
            messageBox = QMessageBox()
            messageBox.setWindowTitle('Concept Map')
            messageBox.setText('是否保存对文件的更改')
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('是')
            buttonN = messageBox.button(QMessageBox.No)
            buttonN.setText('否')
            buttonN = messageBox.button(QMessageBox.Cancel)
            buttonN.setText('取消')
            messageBox.exec_()

            if messageBox.clickedButton() == buttonY:
                if not self.filename:  # 新文件
                    res = self.saveasfile()
                    if not res:
                        event.ignore()  # 未完成保存等同取消
                else:  # 已有文件
                    self.savefile(self.filename)
            elif messageBox.clickedButton() == buttonN:
                event.ignore()  # 不保存
            else:
                pass  # 取消

    def paintEvent(self, event):
        pen = QPainter(self)
        if not pen.isActive():
            pen.begin(self)
        
        if self.draw and hasattr(self, 'lines'):
            for s in self.lines:
                for l in self.lines[s]:
                    ss = self.window.findChild(QLineEdit, s)
                    ee = self.window.findChild(QLineEdit, l)
                    line = QLineF(ss.x() + ss.width()/2, ss.y() + ss.height()/2, 
                    ee.x() + ee.width()/2, ee.y() + ee.height()/2)
                    line.setLength(line.length())
                    pen.setPen(QPen(Qt.darkRed, 2, Qt.DashLine))
                    pen.drawLine(line)
                    self.drawarrow(pen, line, ss, ee)

        if hasattr(self, 'press_e'):
            if self.press_s and self.press and self.press_e:
                alltag = self.findChildren(Newlable)
                for index,tag in enumerate(alltag):
                    area = QRect(QPoint(tag.x(),tag.y()),
                                QPoint(tag.x()+tag.width(),tag.y()+tag.height()))
                    if area.contains(self.press_s):
                        return None
                pen.setPen(QPen(Qt.black, 1, Qt.DashLine))
                scene = QGraphicsScene()
                scene.setSceneRect(0, 0, self.width(), self.height())
                rect = QRectF(self.press_s, self.press_e)
                pen.drawRect(rect)

    def drawarrow(self, pen, line, s, e):
        v = line.unitVector()
        v.setLength(15)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(line.dx() / 2, line.dy() / 2))

        n = v.normalVector()  # 法向量
        n.setLength(n.length() * 0.5)  # 这里设定箭头的宽度

        n2 = n.normalVector().normalVector()

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()

        pen.setPen(QPen(Qt.darkRed, 2, Qt.SolidLine))
        pen.drawPolygon(p1, p2, p3)

        # 记录箭头位置和头尾节点
        l = min(p1.x(), p2.x(), p3.x())
        r = max(p1.x(), p2.x(), p3.x())
        t = max(p1.y(), p2.y(), p3.y())
        f = min(p1.y(), p2.y(), p3.y())
        value = [l, r, t, f, s, e]
        if value not in self.arrows.values():
            for k in self.arrows:
                if s == self.arrows[k][-2] and s == self.arrows[k][-1]:
                    self.arrows.pop(k)
            self.arrows[self.arrows_num] = value
            self.arrows_num += 1

    def drawline_pt(self, s, e):
        self.draw = True
        # 两点间已有连线
        if e.objectName() in self.lines:
            if s.objectName() in self.lines[e.objectName()]:
                # self.lines[s.objectName()].append(e.objectName())
                # self.lines[e.objectName()].remove(s.objectName())
                # todo:添加反向线
                return 0
        # 无s点记录
        if s.objectName() not in self.lines:
            self.lines[s.objectName()] = [e.objectName()]
        # 有s点记录
        else:
            # 删除现有连线
            if e.objectName() in self.lines[s.objectName()]:
                self.lines[s.objectName()].remove(e.objectName())
            # 添加新连线
            else:
                self.lines[s.objectName()].append(e.objectName())
        self.update()

    def mousePressEvent(self, event):
        # 标记按下和坐标
        self.press = True
        self.press_s = event.pos()

        alltag = self.findChildren(QLineEdit)
        for tag in alltag:
            # 删除无内容tag
            if not tag.text():
                tag.deltag()
            else:
                if tag.state:
                    tag.setReadOnly(True)
                    tag.setAcceptDrops(False)
                    if tag.state == 'edit':
                        if tag.x() < event.x() and event.x() < tag.x() + 150 \
                                and tag.y() < event.y() and event.y() < tag.y() + 90:
                            # TODO:想办法解决光标和鼠标事件冲突
                            return None
                        else:
                            tag.setSelection(len(tag.text()), len(tag.text()))
                            tag.state = None
                    if not tag.Bstate:
                        tag.setStyleSheet(tag.sheet['None'])
                    else:
                        tag.setStyleSheet(tag.sheet['B'])
                # break

        for key in self.arrows:
            x = event.x()
            y = event.y()
            if x >= self.arrows[key][0] and x <= self.arrows[key][1] and \
                    y <= self.arrows[key][2] and y >= self.arrows[key][3]:
                new = self.window.inittag(x, y)
                new.show()
                self.drawline_pt(self.arrows[key][-2], new)
                self.drawline_pt(new, self.arrows[key][-1])
                self.lines[self.arrows[key][-2].objectName()].remove(self.arrows[key][-1].objectName())
                self.arrows.pop(key)
                return None

    def mouseReleaseEvent(self, event):
        self.press = False
        if self.press_s and hasattr(self,'press_e'):
            if self.press_e:
                area = QRect(self.press_s, self.press_e)
                self.press = False
                self.press_s = None
                self.press_e = None
                self.update()
                self.selects = []
                alltag = self.findChildren(Newlable)
                for tag in alltag:
                    if area.contains(tag.x() + 75, tag.y() + 30):
                        self.selects.append(tag)
                        tag.state = 'select'
                        tag.setStyleSheet(tag.sheet[tag.state])

    def mouseMoveEvent(self, event):
        if self.press:
            self.press_e = event.pos()
            self.update()
        else:
            x = event.x()
            y = event.y()
            flag = False
            if len(self.arrows) > 0:
                for key in self.arrows:
                    if x >= self.arrows[key][0] and x <= self.arrows[key][1] and \
                            y <= self.arrows[key][2] and y >= self.arrows[key][3]:
                        flag = True
                    else:
                        pass
            if flag:
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, event):
        wx = self.x()
        wy = self.y()
        x = event.globalX()
        y = event.globalY()

        self.inittag(x - wx, y - wy)

    def inittag(self, x, y):
        self.changed = True
        name = 'tag' + str(self.num)
        exec('self.%s = Newlable(self)' % name)
        exec('self.%s.setGeometry(x - 90, y - 75, 180, 50)' % name)
        exec('self.%s.show()' % name)
        exec('self.%s.setObjectName("%s")' % (name, name))
        self.nodes[self.num] = {}
        self.num += 1
        return eval('self.%s' % name)

    def modify_txt(self):
        self.tag1.setTextInteractionFlags(Qt.TextEditorInteraction)

    # 另存为
    def saveasfile(self):
        self.filename = self.savefile()
        if self.filename:
            self.setWindowTitle("Concept map - " + os.path.basename(self.filename))
        return self.filename

    # 保存
    def savefile(self, filename=None):
        if not filename:
            FileName, _ = QFileDialog.getSaveFileName(self, "保存概念图", "", "CM Files(*.xml)")
            if not FileName:
                return None
        else:
            FileName = filename

        self.nodes = {}
        alltag = self.findChildren(QLineEdit)

        # 提取信息
        for index, tag in enumerate(alltag):
            self.nodes[tag.objectName()] = {'Info': {'Width': str(tag.width()),
                                                     'FontSize': str(tag.fontInfo().pointSize()),
                                                     'ID': tag.objectName(),
                                                     'Position': ('%d,%d') % (tag.pos().x(), tag.pos().y()),
                                                     'Bstate': str(tag.Bstate)},
                                            'string': tag.text()}
            if tag.objectName() in self.lines:
                cons = ','.join(self.lines[tag.objectName()])
                self.nodes[tag.objectName()]['connects'] = cons

        # 通过信息构造xml
        root = ET.Element('CM_File')  # 创建首节点
        fid = ET.SubElement(root, 'Fid')  # 增加子节点
        fid.text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        nodes = ET.SubElement(root, 'Notes')
        for k in self.nodes:
            node = ET.SubElement(nodes, 'Note', attrib=self.nodes[k]['Info'])
            string = ET.SubElement(node, 'String')
            string.text = self.nodes[k]['string']
            connect = ET.SubElement(node, 'ConnectedNoteIDs')
            if 'connects' in self.nodes[k]:
                connect.text = self.nodes[k]['connects']
            else:
                connect.text = 'None'

        w = ET.ElementTree(root)

        w.write(FileName, 'utf-8', xml_declaration=True)
        return FileName

    def openfile(self):
        alltag = self.window.findChildren(QLineEdit)
        if len(alltag) == 0:  # 当前无标签 在原窗口打开
            new = self
        else:  # 当前有标签 新建窗口
            self.new = Mainwindow()
            self.new.move(self.x() + 100, self.y() + 100)
            new = self.new

        FileName, _ = QFileDialog.getOpenFileName \
            (new,
             "选取文件",
             "",
             "XML Files (*.xml);;Scap File(*.scap);;All File(*.*)")

        if not FileName:
            return 0
        else:
            new.filename = FileName
            new.setWindowTitle("Concept map - " + os.path.basename(new.filename))

        tree = ET.parse(FileName)
        # 读取点数据
        nodes = tree.find('Notes')
        for node in nodes:
            info = node.attrib
            x, y = info['Position'].split(',')
            tag = new.inittag(int(float(x)) + 90, int(float(y)) + 75)  # 适应正常初始化，添加偏移量

            nid = info['ID']
            if 'tag' not in nid:
                num = int(nid)
                nid = 'tag' + str(nid)
            else:
                num = int(nid[3:])
            tag.setText(node.find('String').text)
            tag.setObjectName(nid)
            tag.state = None
            tag.setReadOnly(True)
            tag.setSelection(len(tag.text()), len(tag.text()))
            tag.setStyleSheet(tag.sheet['None'])

            # 更新tag计数 防止计数冲突
            if num > new.num:
                new.num = num

            # 获取链接信息
            cons_n = node.find('ConnectedNoteIDs')

            if cons_n != None:
                cons_t = cons_n.text
                if cons_t not in ['None', None]:
                    cons = cons_t.split(',')
                    temp_n = []
                    if '-' in cons_t:  # 适应sapple文件格式
                        for c in cons:
                            sn, en = [int(n) for n in c.split('-')]
                            ns = ['tag' + str(n) for n in range(sn, en + 1)]
                            temp_n += ns
                        cons = temp_n
                    else:
                        if 'tag' not in cons_t:
                            for c in cons:
                                temp_n.append('tag' + c.strip())
                            cons = temp_n
                    new.lines[nid] = cons

            if info['Bstate'] == 'True':
                tag.Bstate = True
                tag.setStyleSheet(tag.sheet['B'])
            tag.show()

        new.num += 1  # 更新计数器，防止与读取内容冲突
        new.draw = True
        new.update()
        new.show()

    def newfile(self):
        self.new = Mainwindow()
        self.new.move(self.x() + 100, self.y() + 100)
        self.new.show()


class Dlabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(None, parent)
        self.window = self.parentWidget()
        self.setAcceptDrops(True)
        self.setStyleSheet("border-width:0px;border-style: None; "
                           "border-radius: 15px;background-color:rgb(240,240,240)")

    def leaveEvent(self, event):
        self.setStyleSheet("border-width:0px;border-style: None; "
                           "border-radius: 15px;background-color:rgb(240,240,240)")
        self.window.setCursor(QCursor(Qt.ArrowCursor))

    def dropEvent(self, event):
        text = event.mimeData().text()
        texts = text.split('\n')
        if self.objectName() == 'tag':
            for index, tag in enumerate(texts):
                new = self.window.inittag(0, 0)
                new.move(self.width() + 20, self.y() + (index + 1) * 80)
                new.setStyleSheet(new.sheet['B'])
                new.Bstate = True
                new.state = None
                new.setReadOnly(True)
                new.setText(tag)
        else:
            for index, tag in enumerate(texts):
                new = self.window.inittag(0, 0)
                new.move(self.window.width() - self.width() - new.width() - 20, self.y() + (index + 1) * 80)
                new.setStyleSheet(new.sheet['None'])
                new.setReadOnly(True)
                new.state = None
                new.setText(tag)

        # TODO：检测生成的tag位置 防止多次生成重叠

    def dragLeaveEvent(self, event):
        self.setStyleSheet("border-width:0px;border-style: None; "
                           "border-radius: 15px;background-color:rgb(240,240,240)")
        self.window.setCursor(QCursor(Qt.ArrowCursor))

    def dragEnterEvent(self, event):
        self.setStyleSheet("border-width:0px;border-style: None; "
                           "border-radius: 15px;background-color:grey")
        self.window.setCursor(QCursor(Qt.DragCopyCursor))
        # 接受事件 将事件转到dropevent
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Mainwindow()
    win.show()
    sys.exit(app.exec_())
