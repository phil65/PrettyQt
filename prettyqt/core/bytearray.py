from qtpy import QtCore


class ByteArray(QtCore.QByteArray):
    def __reduce__(self):
        return self.__class__, (bytes(self),)
