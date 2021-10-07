from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict


TYPES = bidict(
    variable=QtGui.QTextLength.Type.VariableLength,
    fixed=QtGui.QTextLength.Type.FixedLength,
    percentage=QtGui.QTextLength.Type.PercentageLength,
)

TypeStr = Literal["variable", "fixed", "percentage"]


class TextLength(QtGui.QTextLength):
    def __repr__(self):
        return f"{type(self).__name__}({self.type()}, {self.rawValue()})"

    def get_type(self) -> TypeStr:
        """Return type of this length object.

        Returns:
            timer type
        """
        return TYPES.inverse[self.type()]


if __name__ == "__main__":
    length = TextLength()
