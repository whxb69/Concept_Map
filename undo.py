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
                self._window.inittag(self._tlist['x'], self._tlist['y'], name=name)

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

#触碰连线操作 其余附带连线不包括
class UndoDrawLine(QUndoCommand):
    def __init__(self,window, llist, first):
        QUndoCommand.__init__(self)
        self._window = window
        self._llist = llist
        self._first = first

    def undo(self):
        for start,end in self._llist:
            self._window.lines[start].remove(end)
        self._window.update()

    def redo(self):
        if not self._first:
            self._window.drawline_pt(self._start,self._end)

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
        pass

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
        pass

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
        pass
