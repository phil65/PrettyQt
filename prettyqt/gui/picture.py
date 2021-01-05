from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui


QtGui.QPicture.__bases__ = (gui.PaintDevice,)


class Picture(QtGui.QPicture):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)
