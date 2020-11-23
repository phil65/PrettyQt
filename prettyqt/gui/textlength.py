# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt.utils import bidict

TYPES = bidict(
    variable=QtGui.QTextLength.VariableLength,
    fixed=QtGui.QTextLength.FixedLength,
    percentage=QtGui.QTextLength.PercentageLength,
)


class TextLength(QtGui.QTextLength):
    def __repr__(self):
        return f"TextLength({self.type()}, {self.rawValue()})"

    def get_type(self) -> str:
        """Return type of this length object.

        Possible values: "variable", "fixed", "percentage"

        Returns:
            timer type
        """
        return TYPES.inv[self.type()]


if __name__ == "__main__":
    length = TextLength()
