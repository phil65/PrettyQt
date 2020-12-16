from typing import Tuple

from qtpy import QtGui

from prettyqt import core, gui


QtGui.QImage.__bases__ = (gui.PaintDevice,)


class Image(QtGui.QImage):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __setitem__(self, index: Tuple[int, int], value):
        self.setPixel(index[0], index[1], value)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getitem__(self, index: Tuple[int, int]):
        return self.pixel(index[0], index[1])

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)


if __name__ == "__main__":
    image = Image()
    bytes(image)
