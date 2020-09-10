from typing import Tuple

from qtpy import QtGui

from prettyqt import gui, core


QtGui.QImage.__bases__ = (gui.PaintDevice,)


class Image(QtGui.QImage):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def __setitem__(self, index: Tuple[int, int], value):
        self.setPixel(index[0], index[1], value)

    def __getitem__(self, index: Tuple[int, int]):
        return self.pixel(index[0], index[1])


if __name__ == "__main__":
    image = Image()
