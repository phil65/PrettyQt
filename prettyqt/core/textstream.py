from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


FieldAlignmentStr = Literal["left", "right", "center", "accounting_style"]

FIELD_ALIGNMENT: bidict[FieldAlignmentStr, QtCore.QTextStream.FieldAlignment] = bidict(
    left=QtCore.QTextStream.FieldAlignment.AlignLeft,
    right=QtCore.QTextStream.FieldAlignment.AlignRight,
    center=QtCore.QTextStream.FieldAlignment.AlignCenter,
    accounting_style=QtCore.QTextStream.FieldAlignment.AlignAccountingStyle,
)

NumberFlagStr = Literal[
    "show_base", "force_point", "force_sign", "uppercase_base", "uppercase_digits"
]

NUMBER_FLAGS: bidict[NumberFlagStr, QtCore.QTextStream.NumberFlag] = bidict(
    show_base=QtCore.QTextStream.NumberFlag.ShowBase,
    force_point=QtCore.QTextStream.NumberFlag.ForcePoint,
    force_sign=QtCore.QTextStream.NumberFlag.ForceSign,
    uppercase_base=QtCore.QTextStream.NumberFlag.UppercaseBase,
    uppercase_digits=QtCore.QTextStream.NumberFlag.UppercaseDigits,
)

RealNumberNotationStr = Literal["scientific", "fixed", "smart"]

REAL_NUMBER_NOTATION: bidict[
    RealNumberNotationStr, QtCore.QTextStream.RealNumberNotation
] = bidict(
    scientific=QtCore.QTextStream.RealNumberNotation.ScientificNotation,
    fixed=QtCore.QTextStream.RealNumberNotation.FixedNotation,
    smart=QtCore.QTextStream.RealNumberNotation.SmartNotation,
)

StatusStr = Literal["ok", "read_past_end", "read_corrupt_data", "write_failed"]

STATUS: bidict[StatusStr, QtCore.QTextStream.Status] = bidict(
    ok=QtCore.QTextStream.Status.Ok,
    read_past_end=QtCore.QTextStream.Status.ReadPastEnd,
    read_corrupt_data=QtCore.QTextStream.Status.ReadCorruptData,
    write_failed=QtCore.QTextStream.Status.WriteFailed,
)


class TextStream(QtCore.QTextStream):
    """Convenient interface for reading and writing text."""

    def set_field_alignment(
        self, alignment: FieldAlignmentStr | QtCore.QTextStream.FieldAlignment
    ):
        """Set the field alignment.

        Args:
            alignment: field alignment
        """
        self.setFieldAlignment(FIELD_ALIGNMENT.get_enum_value(alignment))

    def get_field_alignment(self) -> FieldAlignmentStr:
        """Get current field alignment.

        Returns:
            current field alignment
        """
        return FIELD_ALIGNMENT.inverse[self.fieldAlignment()]

    def set_status(self, status: StatusStr | QtCore.QTextStream.Status):
        """Set the status.

        Args:
            status: status
        """
        self.setStatus(STATUS.get_enum_value(status))

    def get_status(self) -> StatusStr:
        """Get current status.

        Returns:
            current status
        """
        return STATUS.inverse[self.status()]

    def set_real_number_notation(
        self, notation: RealNumberNotationStr | QtCore.QTextStream.RealNumberNotation
    ):
        """Set the real number notation.

        Args:
            notation: real number notation
        """
        self.setRealNumberNotation(REAL_NUMBER_NOTATION.get_enum_value(notation))

    def get_real_number_notation(self) -> RealNumberNotationStr:
        """Get current real number notation.

        Returns:
            current real number notation
        """
        return REAL_NUMBER_NOTATION.inverse[self.realNumberNotation()]

    def read_lines(self) -> Iterator[str]:
        while True:
            if msg := self.readLine():
                yield msg
            else:
                return

    def get_number_flags(self) -> list[NumberFlagStr]:
        return NUMBER_FLAGS.get_list(self.numberFlags())

    def set_number_flags(self, *flags: NumberFlagStr):
        flag = NUMBER_FLAGS.merge_flags(flags)
        self.setNumberFlags(flag)


if __name__ == "__main__":
    stream = TextStream(QtCore.QByteArray(b"Test"))
    print(repr(stream))
