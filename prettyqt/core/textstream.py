from typing import Literal

from qtpy import QtCore

from prettyqt.utils import InvalidParamError, bidict


FIELD_ALIGNMENT = bidict(
    left=QtCore.QTextStream.AlignLeft,
    right=QtCore.QTextStream.AlignRight,
    center=QtCore.QTextStream.AlignCenter,
    accounting_style=QtCore.QTextStream.AlignAccountingStyle,
)

FieldAlignmentStr = Literal["left", "right", "center", "accounting_style"]

NUMBER_FLAGS = bidict(
    show_base=QtCore.QTextStream.ShowBase,
    force_point=QtCore.QTextStream.ForcePoint,
    force_sign=QtCore.QTextStream.ForceSign,
    uppercase_base=QtCore.QTextStream.UppercaseBase,
    uppercase_digits=QtCore.QTextStream.UppercaseDigits,
)

NumberFlagStr = Literal[
    "show_base", "force_point", "force_sign", "uppercase_base", "uppercase_digits"
]

REAL_NUMBER_NOTATION = bidict(
    scientific=QtCore.QTextStream.ScientificNotation,
    fixed=QtCore.QTextStream.FixedNotation,
    smart=QtCore.QTextStream.SmartNotation,
)

RealNumberNotationStr = Literal["scientific", "fixed", "smart"]

STATUS = bidict(
    ok=QtCore.QTextStream.Ok,
    read_past_end=QtCore.QTextStream.ReadPastEnd,
    read_corrupt_data=QtCore.QTextStream.ReadCorruptData,
    write_failed=QtCore.QTextStream.WriteFailed,
)

StatusStr = Literal["ok", "read_past_end", "read_corrupt_data", "write_failed"]


class TextStream(QtCore.QTextStream):
    def set_field_alignment(self, alignment: FieldAlignmentStr):
        """Set the field alignment.

        Args:
            alignment: field alignment

        Raises:
            InvalidParamError: invalid field alignment
        """
        if alignment not in FIELD_ALIGNMENT:
            raise InvalidParamError(alignment, FIELD_ALIGNMENT)
        self.setFieldAlignment(FIELD_ALIGNMENT[alignment])

    def get_field_alignment(self) -> FieldAlignmentStr:
        """Get current field alignment.

        Returns:
            current field alignment
        """
        return FIELD_ALIGNMENT.inverse[self.fieldAlignment()]

    def set_status(self, status: StatusStr):
        """Set the status.

        Args:
            status: status

        Raises:
            InvalidParamError: invalid status
        """
        if status not in STATUS:
            raise InvalidParamError(status, STATUS)
        self.setStatus(STATUS[status])

    def get_status(self) -> StatusStr:
        """Get current status.

        Returns:
            current status
        """
        return STATUS.inverse[self.status()]

    def set_real_number_notation(self, notation: RealNumberNotationStr):
        """Set the real number notation.

        Args:
            notation: real number notation

        Raises:
            InvalidParamError: invalid real number notation
        """
        if notation not in REAL_NUMBER_NOTATION:
            raise InvalidParamError(notation, REAL_NUMBER_NOTATION)
        self.setRealNumberNotation(REAL_NUMBER_NOTATION[notation])

    def get_real_number_notation(self) -> RealNumberNotationStr:
        """Get current real number notation.

        Returns:
            current real number notation
        """
        return REAL_NUMBER_NOTATION.inverse[self.realNumberNotation()]


if __name__ == "__main__":
    matcher = TextStream("Test")
    print(repr(matcher))
