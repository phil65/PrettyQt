# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui, core


QtGui.QImage.__bases__ = (gui.PaintDevice,)


class Image(QtGui.QImage):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)


if __name__ == "__main__":
    image = Image()
