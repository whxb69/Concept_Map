from PyQt5.QtWidgets import QUndoCommand

#建立tag 输入tag list
class UndoInitTag(QUndoCommand):
    def __init__(self, window, tlist, first=False):
        QUndoCommand.__init__(self)
        self._tlist = tlist
        self._first = first
        self._window = window

    def undo(self):
        for name in self._tlist:
            self._window.deleteTag(name)

    def redo(self):
        if not self._first:
            for name in self._tlist:
                tag = self._window.inittag(self._tlist[name]['x'], self._tlist[name]['y'], name=name)
                if self._tlist[name]['B']:
                    tag.Bstate=True
                    tag.stateChanged.emit('None')
        else:
            self._first = False

#删除tag 输入tag list
class UndoDelTag(QUndoCommand):
    def __init__(self, window, dlist, llist, first=False):
        QUndoCommand.__init__(self)
        self._dlist = dlist#tag list
        self._llist = llist#line list
        self._window = window
        self._first = first

    def undo(self):
        for name in self._dlist:
            x = self._dlist[name]['x']
            y = self._dlist[name]['y']
            self._window.inittag(x, y, name=name)
        for start,end in self._llist:
            self._window.drawline_pt(start,end)

    def redo(self):
        if not self._first:
            for name in self._dlist:
                self._window.deleteTag(name)
        else:
            self._first = False

#触碰连线操作 其余附带连线不包括
class UndoDrawLine(QUndoCommand):
    def __init__(self,window, llist, first=False):
        QUndoCommand.__init__(self)
        self._window = window
        self._llist = llist
        self._first = first

    def undo(self):
        for start,end in self._llist:
            if end in self._window.lines[start]:
                self._window.lines[start].remove(end)
        self._window.update()

    def redo(self):
        if not self._first:
            for start,end in self._llist:
                self._window.drawline_pt(start,end)
            self._window.update()
        else:
            self._first = False

#剪切到粘贴
class UndoPaste(QUndoCommand):
    def __init__(self,window, tlist, first):
        QUndoCommand.__init__(self)
        self._tlist = tlist
        self._window = window
        self._first = first

    def undo(self):
        for name in self._tlist:
            if name in self._window.lines:
                self._window.lines.pop(name)
            self._window.deleteTag(name)

    def redo(self):
        if not self._first:
            pass
        else:
            self._first = False

#移动
class UndoMove(QUndoCommand):
    def __init__(self,window,tlist,first):
        QUndoCommand.__init__(self)
        self._tlist = tlist
        self._window = window
        self._first = first

    def undo(self):
        for name in self._tlist:
            tag = self._tlist[name]['obj']
            tag.move(self._tlist[name]['x'],self._tlist[name]['y'])

        self._window.update()

    def redo(self):
        if not self._first:
            for name in self._tlist:
                tag = self._tlist[name]['obj']
                tag.move(self._tlist[name]['nx'],self._tlist[name]['ny'])
        else:
            self._first = False

#新建连接
class UndoNewlink(QUndoCommand):
    def __init__(self,window,newtag,selects,first):
        QUndoCommand.__init__(self)
        self._newtag = newtag
        self._selects = selects
        self._window = window
        self._first = first
    
    def undo(self):
        for tag in self._selects:
            self._window.lines[tag].remove(self._newtag)
        self._window.deleteTag(self._newtag)

    def redo(self):
        if not self._first:
            pass
        else:
            self._first = False

#点击箭头新建标签
class UndoArrowtag(QUndoCommand):
    def __init__(self,window,tinfo,start,end,first):
        QUndoCommand.__init__(self)
        self._tag = tinfo['obj']
        self._start = start
        self._end = end
        self._x = tinfo['x']
        self._y = tinfo['y']
        self._window = window
        self._first = first
    
    def undo(self):
        self._window.deleteTag(self._tag.objectName())
        self._window.drawline_pt(self._start,self._end)

    def redo(self):
        if not self._first:
            new = self._window.inittag(self._x, self._y)
            new.show()
            self._window.drawline_pt(self._start, new)
            self._window.drawline_pt(new, self._end)
            self._window.lines[self._start.objectName()].remove(self._end.objectName())
            self._window.arrows.pop(key)
            self._tag = new
        else:
            self._first = False