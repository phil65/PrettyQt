from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict


WORD_WRAP_MODE = bidict(
    none=QtGui.QTextOption.NoWrap,
    word=QtGui.QTextOption.WordWrap,
    anywhere=QtGui.QTextOption.WrapAnywhere,
    boundary_or_anywhere=QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere,
)

WordWrapModeStr = Literal["none", "word", "anywhere", "boundary_or_anywhere"]


class TextOption(QtGui.QTextOption):
    pass


if __name__ == "__main__":
    doc = TextOption()
