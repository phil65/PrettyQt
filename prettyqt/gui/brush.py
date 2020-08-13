# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import core, gui


class Brush(QtGui.QBrush):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def get_texture_image(self):
        return gui.Image(self.textureImage())
