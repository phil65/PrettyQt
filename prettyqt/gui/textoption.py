from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict


WORD_WRAP_MODE = bidict(
    none=QtGui.QTextOption.WrapMode.NoWrap,
    word=QtGui.QTextOption.WrapMode.WordWrap,
    manual=QtGui.QTextOption.WrapMode.ManualWrap,
    anywhere=QtGui.QTextOption.WrapMode.WrapAnywhere,
    boundary_or_anywhere=QtGui.QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere,
)

WordWrapModeStr = Literal["none", "word", "manual", "anywhere", "boundary_or_anywhere"]

TAB_TYPE = bidict(
    left=QtGui.QTextOption.TabType.LeftTab,
    right=QtGui.QTextOption.TabType.RightTab,
    center=QtGui.QTextOption.TabType.CenterTab,
    delimiter=QtGui.QTextOption.TabType.DelimiterTab,
)

TabTypeStr = Literal["left", "right", "center", "delimiter"]


FLAG = bidict(
    include_trailing_whitespaces=QtGui.QTextOption.Flag.IncludeTrailingSpaces,
    show_tabs_and_spaces=QtGui.QTextOption.Flag.ShowTabsAndSpaces,
    show_separators=QtGui.QTextOption.Flag.ShowLineAndParagraphSeparators,
    show_document_terminator=QtGui.QTextOption.Flag.ShowDocumentTerminator,
    add_space_for_separators=QtGui.QTextOption.Flag.AddSpaceForLineAndParagraphSeparators,
    suppress_colors=QtGui.QTextOption.Flag.SuppressColors,
)

FlagStr = Literal[
    "include_trailing_whitespaces",
    "show_tabs_and_spaces",
    "show_separators",
    "show_document_terminator",
    "add_space_for_separators",
    "suppress_colors",
]


class TextOption(QtGui.QTextOption):
    pass


if __name__ == "__main__":
    doc = TextOption()
