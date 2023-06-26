from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, datatypes


FloatingPointPrecisionStr = Literal["single", "double"]

FLOATING_POINT_PRECISION: bidict[
    FloatingPointPrecisionStr, QtCore.QDataStream.FloatingPointPrecision
] = bidict(
    single=QtCore.QDataStream.FloatingPointPrecision.SinglePrecision,
    double=QtCore.QDataStream.FloatingPointPrecision.DoublePrecision,
)

ByteOrderStr = Literal["big_endian", "little_endian"]

BYTE_ORDER: bidict[ByteOrderStr, QtCore.QDataStream.ByteOrder] = bidict(
    big_endian=QtCore.QDataStream.ByteOrder.BigEndian,
    little_endian=QtCore.QDataStream.ByteOrder.LittleEndian,
)

StatusStr = Literal["ok", "read_past_end", "read_corrupt_data", "write_failed"]

STATUS: bidict[StatusStr, QtCore.QDataStream.Status] = bidict(
    ok=QtCore.QDataStream.Status.Ok,
    read_past_end=QtCore.QDataStream.Status.ReadPastEnd,
    read_corrupt_data=QtCore.QDataStream.Status.ReadCorruptData,
    write_failed=QtCore.QDataStream.Status.WriteFailed,
)


class DataStream(QtCore.QDataStream):
    def set_byte_order(self, order: ByteOrderStr | QtCore.QDataStream.ByteOrder):
        """Set byte order.

        Args:
            order: byte order to use
        """
        self.setByteOrder(BYTE_ORDER.get_enum_value(order))

    def get_byte_order(self) -> ByteOrderStr:
        """Return byte order.

        Returns:
            byte order
        """
        return BYTE_ORDER.inverse[self.byteOrder()]

    def set_status(self, status: StatusStr):
        """Set status.

        Args:
            status: status to use
        """
        self.setStatus(STATUS.get_enum_value(status))

    def get_status(self) -> StatusStr:
        """Return status.

        Returns:
            status
        """
        return STATUS.inverse[self.status()]

    def set_floating_point_precision(
        self,
        precision: FloatingPointPrecisionStr | QtCore.QDataStream.FloatingPointPrecision,
    ):
        """Set floating point precision.

        Args:
            precision: floating point precision
        """
        self.setFloatingPointPrecision(FLOATING_POINT_PRECISION.get_enum_value(precision))

    def get_floating_point_precision(self) -> FloatingPointPrecisionStr:
        """Return floating point precision.

        Returns:
            floating point precision
        """
        return FLOATING_POINT_PRECISION.inverse[self.floatingPointPrecision()]

    @classmethod
    def create_bytearray(cls, data: datatypes.QtSerializableType) -> QtCore.QByteArray:
        ba = QtCore.QByteArray()
        stream = cls(ba, QtCore.QIODeviceBase.OpenModeFlag.WriteOnly)
        stream << data
        return ba

    @classmethod
    def write_bytearray(
        cls, ba: datatypes.ByteArrayType, write_to: datatypes.QtSerializableType
    ):
        ba = datatypes.to_bytearray(ba)
        stream = cls(ba, QtCore.QIODeviceBase.OpenModeFlag.ReadOnly)
        stream >> write_to

    @classmethod
    def copy_data(
        cls, source: datatypes.QtSerializableType, dest: datatypes.QtSerializableType
    ):
        ba = cls.create_bytearray(source)
        cls.write_bytearray(ba, dest)
