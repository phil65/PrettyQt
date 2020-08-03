# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


FLOAT_PRECISION = bidict(
    single=QtCore.QDataStream.SinglePrecision, double=QtCore.QDataStream.DoublePrecision,
)

BYTE_ORDER = bidict(
    big_endian=QtCore.QDataStream.BigEndian,
    little_endian=QtCore.QDataStream.LittleEndian,
)


class DataStream(QtCore.QDataStream):
    def set_byte_order(self, order: str):
        """Set byte order.

        valid values are: "big_endian", "little endian"

        Args:
            order: byte order to use

        Raises:
            InvalidParamError: invalid order
        """
        if order not in BYTE_ORDER:
            raise InvalidParamError(order, BYTE_ORDER)
        self.setByteOrder(BYTE_ORDER[order])

    def get_byte_order(self) -> bool:
        """Return byte order.

        possible values are "big_endian", "little_endian"

        Returns:
            byte order
        """
        return BYTE_ORDER.inv[self.byteOrder()]

    def set_float_precision(self, precision: str):
        """Set floating point precision.

        valid values are: "single", "double"

        Args:
            precision: floating point precision

        Raises:
            InvalidParamError: invalid precision
        """
        if precision not in FLOAT_PRECISION:
            raise InvalidParamError(precision, FLOAT_PRECISION)
        self.setFloatingPointPrecision(FLOAT_PRECISION[precision])

    def get_float_precision(self) -> bool:
        """Return floating point precision.

        possible values are "single", "double"

        Returns:
            floating point precision
        """
        return FLOAT_PRECISION.inv[self.floatingPointPrecision()]

    @classmethod
    def create_bytearray(cls, data) -> QtCore.QByteArray:
        ba = QtCore.QByteArray()
        stream = cls(ba, core.IODevice.WriteOnly)
        stream << data
        return ba

    @classmethod
    def write_bytearray(cls, ba: QtCore.QByteArray, write_to):
        stream = cls(ba, core.IODevice.ReadOnly)
        stream >> write_to

    @classmethod
    def copy_data(cls, source, dest):
        ba = cls.create_bytearray(source)
        cls.write_bytearray(ba, dest)
