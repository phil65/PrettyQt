from qtpy import QtGui

from prettyqt import core


class Region(QtGui.QRegion):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)
