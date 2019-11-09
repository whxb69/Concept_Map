from PyQt5.QtWidgets import QUndoCommand


class UndoInitTag(QUndoCommand):
    def __init__(self, tag, name, x, y,first=False):
        QUndoCommand.__init__(self)
        self._name = name
        self._x = x
        self._y = y
        self._tag = tag
        self._first = first

    def undo(self):
        self._tag.deltag()

    def redo(self):
        if not self._first:
            self._tag.window.inittag(self._x, self._y, name=self._name)


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