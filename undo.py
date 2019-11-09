from PyQt5.QtWidgets import QUndoCommand


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


class UndoDelTag(QUndoCommand):
    def __init__(self, window, dlist, llist, first=False):
        QUndoCommand.__init__(self)
        self._dlist = dlist
        self._llist = llist
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

class UndoDrawLine(QUndoCommand):
    def __init__(self,window, start, end, first):
        QUndoCommand.__init__(self)
        self._window = window
        self._start = start
        self._end = end
        self._first = first

    def undo(self):
        self._window.lines[self._start].remove(self._end)
        self._window.update()

    def redo(self):
        if not self._first:
            self._window.drawline_pt(self._start,self._end)

class UndoPaste(QUndoCommand):
    def __init__(self,window, tlist, llist, first):
        QUndoCommand.__init__(self)
        self._tlist = tlist
        self._llist = llist
        self._window = window
        self._first = first

    def undo(self):
        pass

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
