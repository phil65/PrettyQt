from qtpy import QtCore

from prettyqt.utils import bidict, InvalidParamError

FIELD_ALIGNMENT = bidict(
    left=QtCore.QTextStream.AlignLeft,
    right=QtCore.QTextStream.AlignRight,
    center=QtCore.QTextStream.AlignCenter,
    accounting_style=QtCore.QTextStream.AlignAccountingStyle,
)

NUMBER_FLAGS = bidict(
    show_base=QtCore.QTextStream.ShowBase,
    force_point=QtCore.QTextStream.ForcePoint,
    force_sign=QtCore.QTextStream.ForceSign,
    uppercase_base=QtCore.QTextStream.UppercaseBase,
    uppercase_digits=QtCore.QTextStream.UppercaseDigits,
)

REAL_NUMBER_NOTATION = bidict(
    scientific=QtCore.QTextStream.ScientificNotation,
    fixed=QtCore.QTextStream.FixedNotation,
    smart=QtCore.QTextStream.SmartNotation,
)

STATUS = bidict(
    ok=QtCore.QTextStream.Ok,
    read_past_end=QtCore.QTextStream.ReadPastEnd,
    read_corrupt_data=QtCore.QTextStream.ReadCorruptData,
    write_failed=QtCore.QTextStream.WriteFailed,
)


class TextStream(QtCore.QTextStream):
    def set_field_alignment(self, alignment: str):
        """Set the field alignment.

        Valid values are "left", "right", "center", "accounting_style"

        Args:
            alignment: field alignment

        Raises:
            InvalidParamError: invalid field alignment
        """
        if alignment not in FIELD_ALIGNMENT:
            raise InvalidParamError(alignment, FIELD_ALIGNMENT)
        self.setFieldAlignment(FIELD_ALIGNMENT[alignment])

    def get_field_alignment(self) -> str:
        """Get current field alignment.

        Possible values are "left", "right", "center", "accounting_style"

        Returns:
            current field alignment
        """
        return FIELD_ALIGNMENT.inverse[self.fieldAlignment()]

    def set_status(self, status: str):
        """Set the status.

        Valid values are "ok", "read_past_end", "read_corrupt_data", "write_failed"

        Args:
            status: status

        Raises:
            InvalidParamError: invalid status
        """
        if status not in STATUS:
            raise InvalidParamError(status, STATUS)
        self.setStatus(STATUS[status])

    def get_status(self) -> str:
        """Get current status.

        Possible values are "ok", "read_past_end", "read_corrupt_data", "write_failed"

        Returns:
            current status
        """
        return STATUS.inverse[self.status()]

    def set_real_number_notation(self, notation: str):
        """Set the real number notation.

        Valid values are "scientific", "fixed", "smart"

        Args:
            notation: real number notation

        Raises:
            InvalidParamError: invalid real number notation
        """
        if notation not in REAL_NUMBER_NOTATION:
            raise InvalidParamError(notation, REAL_NUMBER_NOTATION)
        self.setRealNumberNotation(REAL_NUMBER_NOTATION[notation])

    def get_real_number_notation(self) -> str:
        """Get current real number notation.

        Possible values are "scientific", "fixed", "smart"

        Returns:
            current real number notation
        """
        return REAL_NUMBER_NOTATION.inverse[self.realNumberNotation()]


if __name__ == "__main__":
    matcher = TextStream("Test")
    print(repr(matcher))
