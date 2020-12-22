from qtpy import QtCore


class ByteArray(QtCore.QByteArray):
    def __reduce__(self):
        return type(self), (bytes(self),)
