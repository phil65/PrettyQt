from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict


WORD_WRAP_MODE = bidict(
    none=QtGui.QTextOption.WrapMode.NoWrap,
    word=QtGui.QTextOption.WrapMode.WordWrap,
    anywhere=QtGui.QTextOption.WrapMode.WrapAnywhere,
    boundary_or_anywhere=QtGui.QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere,
)

WordWrapModeStr = Literal["none", "word", "anywhere", "boundary_or_anywhere"]


class TextOption(QtGui.QTextOption):
    pass


if __name__ == "__main__":
    doc = TextOption()
