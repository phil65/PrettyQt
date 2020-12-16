from qtpy import QtGui

from prettyqt import constants, core, gui


class Brush(QtGui.QBrush):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_color()!r}, {self.get_style()!r})"

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def get_texture_image(self) -> gui.Image:
        return gui.Image(self.textureImage())

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_style(self) -> constants.PatternStr:
        return constants.PATTERN.inv[self.style()]


if __name__ == "__main__":
    b = Brush()
    print(repr(b))
