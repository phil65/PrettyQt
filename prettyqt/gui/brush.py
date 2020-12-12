from qtpy import QtGui

from prettyqt import core, gui


class Brush(QtGui.QBrush):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def get_texture_image(self):
        return gui.Image(self.textureImage())
