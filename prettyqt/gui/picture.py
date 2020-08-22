# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui, core


QtGui.QPicture.__bases__ = (gui.PaintDevice,)


class Picture(QtGui.QPicture):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)
