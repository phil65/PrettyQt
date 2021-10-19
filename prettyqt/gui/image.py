from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui


QtGui.QImage.__bases__ = (gui.PaintDevice,)


class Image(QtGui.QImage):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __setitem__(self, index: tuple[int, int], value):
        self.setPixel(index[0], index[1], value)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getitem__(self, index: tuple[int, int]):
        return self.pixel(index[0], index[1])

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    @classmethod
    def from_ndarray(cls, arr) -> Image:
        import numpy as np

        height, width, channel = arr.shape
        if arr.dtype in {np.float32, np.float64}:
            arr = (255 * arr).round()
        arr = arr.astype(np.uint8)
        return cls(arr.data, width, height, channel * width, cls.Format.Format_RGB888)

    def invert_pixels(self, invert_alpha: bool = False):
        self.invertPixels(
            self.InvertMode.InvertRgba if invert_alpha else self.InvertMode.InvertRgb
        )


if __name__ == "__main__":
    image = Image()
    bytes(image)
