from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt.qt import QtCore


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class SerializeMixin:
    def __getstate__(self):
        ba = self.create_bytearray()
        return ba.data()

    def __setstate__(self, ba):
        self.write_bytearray(ba)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        return self.__getstate__()

    def create_bytearray(self) -> QtCore.QByteArray:
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODeviceBase.OpenModeFlag.WriteOnly)
        stream << self
        return ba

    def write_bytearray(self, ba: datatypes.ByteArrayType):
        if isinstance(ba, str):
            ba = ba.encode()
        if not isinstance(ba, QtCore.QByteArray):
            ba = QtCore.QByteArray(ba)
        stream = QtCore.QDataStream(ba, QtCore.QIODeviceBase.OpenModeFlag.ReadOnly)
        stream >> self

    def copy_data_to(self, dest: datatypes.QtSerializableType):
        ba = self.create_bytearray()
        stream = QtCore.QDataStream(ba, QtCore.QIODeviceBase.OpenModeFlag.ReadOnly)
        stream >> dest
