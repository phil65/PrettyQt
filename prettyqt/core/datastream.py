from typing import Literal, Union

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


FLOAT_PRECISION = bidict(
    single=QtCore.QDataStream.SinglePrecision,
    double=QtCore.QDataStream.DoublePrecision,
)

FloatPrecisionStr = Literal["single", "double"]

BYTE_ORDER = bidict(
    big_endian=QtCore.QDataStream.BigEndian,
    little_endian=QtCore.QDataStream.LittleEndian,
)

ByteOrderStr = Literal["big_endian", "little_endian"]


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

    def set_float_precision(self, precision: FloatPrecisionStr):
        """Set floating point precision.

        Args:
            precision: floating point precision

        Raises:
            InvalidParamError: invalid precision
        """
        if precision not in FLOAT_PRECISION:
            raise InvalidParamError(precision, FLOAT_PRECISION)
        self.setFloatingPointPrecision(FLOAT_PRECISION[precision])

    def get_float_precision(self) -> FloatPrecisionStr:
        """Return floating point precision.

        Returns:
            floating point precision
        """
        return FLOAT_PRECISION.inverse[self.floatingPointPrecision()]

    @classmethod
    def create_bytearray(cls, data) -> QtCore.QByteArray:
        ba = QtCore.QByteArray()
        stream = cls(ba, core.IODevice.WriteOnly)
        stream << data
        return ba

    @classmethod
    def write_bytearray(cls, ba: Union[QtCore.QByteArray, bytes], write_to):
        if not isinstance(ba, QtCore.QByteArray):
            ba = QtCore.QByteArray(ba)
        stream = cls(ba, core.IODevice.ReadOnly)
        stream >> write_to

    @classmethod
    def copy_data(cls, source, dest):
        ba = cls.create_bytearray(source)
        cls.write_bytearray(ba, dest)
