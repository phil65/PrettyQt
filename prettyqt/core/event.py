from qtpy import QtCore


class Event(QtCore.QEvent):
    def __repr__(self):
        return f"{type(self).__name__}({self.type()})"
