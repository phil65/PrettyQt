from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, types


FLOATING_POINT_PRECISION = bidict(
    single=QtCore.QDataStream.FloatingPointPrecision.SinglePrecision,
    double=QtCore.QDataStream.FloatingPointPrecision.DoublePrecision,
)

FloatingPointPrecisionStr = Literal["single", "double"]

BYTE_ORDER = bidict(
    big_endian=QtCore.QDataStream.ByteOrder.BigEndian,
    little_endian=QtCore.QDataStream.ByteOrder.LittleEndian,
)

ByteOrderStr = Literal["big_endian", "little_endian"]

STATUS = bidict(
    ok=QtCore.QDataStream.Status.Ok,
    read_past_end=QtCore.QDataStream.Status.ReadPastEnd,
    read_corrupt_data=QtCore.QDataStream.Status.ReadCorruptData,
    write_failed=QtCore.QDataStream.Status.WriteFailed,
)

StatusStr = Literal["ok", "read_past_end", "read_corrupt_data", "write_failed"]


class DataStream(QtCore.QDataStream):
    def set_byte_order(self, order: ByteOrderStr):
        """Set byte order.

        Args:
            order: byte order to use

        Raises:
            InvalidParamError: invalid order
        """
        if order not in BYTE_ORDER:
            raise InvalidParamError(order, BYTE_ORDER)
        self.setByteOrder(BYTE_ORDER[order])

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

        Raises:
            InvalidParamError: invalid status
        """
        if status not in STATUS:
            raise InvalidParamError(status, STATUS)
        self.setStatus(STATUS[status])

    def get_status(self) -> StatusStr:
        """Return status.

        Returns:
            status
        """
        return STATUS.inverse[self.status()]

    def set_floating_point_precision(self, precision: FloatingPointPrecisionStr):
        """Set floating point precision.

        Args:
            precision: floating point precision

        Raises:
            InvalidParamError: invalid precision
        """
        if precision not in FLOATING_POINT_PRECISION:
            raise InvalidParamError(precision, FLOATING_POINT_PRECISION)
        self.setFloatingPointPrecision(FLOATING_POINT_PRECISION[precision])

    def get_floating_point_precision(self) -> FloatingPointPrecisionStr:
        """Return floating point precision.

        Returns:
            floating point precision
        """
        return FLOATING_POINT_PRECISION.inverse[self.floatingPointPrecision()]

    @classmethod
    def create_bytearray(cls, data: types.QtSerializableType) -> QtCore.QByteArray:
        ba = QtCore.QByteArray()
        stream = cls(ba, core.iodevice.OPEN_MODES["write_only"])
        stream << data
        return ba

    @classmethod
    def write_bytearray(cls, ba: types.ByteArrayType, write_to: types.QtSerializableType):
        if isinstance(ba, str):
            ba = ba.encode()
        if not isinstance(ba, QtCore.QByteArray):
            ba = QtCore.QByteArray(ba)
        stream = cls(ba, core.iodevice.OPEN_MODES["read_only"])
        stream >> write_to

    @classmethod
    def copy_data(cls, source, dest):
        ba = cls.create_bytearray(source)
        cls.write_bytearray(ba, dest)
