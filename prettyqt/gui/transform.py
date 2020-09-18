# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import core


class Transform(QtGui.QTransform):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def __getitem__(self, value) -> float:
        if value[0] == 0:
            if value[1] == 0:
                return self.m11()
            elif value[1] == 1:
                return self.m12()
            elif value[1] == 2:
                return self.m13()
        elif value[0] == 1:
            if value[1] == 0:
                return self.m21()
            elif value[1] == 1:
                return self.m22()
            elif value[1] == 2:
                return self.m23()
        elif value[0] == 2:
            if value[1] == 0:
                return self.m31()
            elif value[1] == 1:
                return self.m32()
            elif value[1] == 2:
                return self.m33()
        raise ValueError(f"Wrong value {value}")


if __name__ == "__main__":
    transform = Transform()
