from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


BoundaryReasonStr = Literal[
    "not_at_boundary",
    "break_opportunity",
    "start_of_item",
    "end_of_item",
    "mandatory_break",
    "soft_hyphen",
]

BOUNDARY_REASONS: bidict[BoundaryReasonStr, QtCore.QTextBoundaryFinder.BoundaryReason] = (
    bidict(
        not_at_boundary=QtCore.QTextBoundaryFinder.BoundaryReason.NotAtBoundary,
        break_opportunity=QtCore.QTextBoundaryFinder.BoundaryReason.BreakOpportunity,
        start_of_item=QtCore.QTextBoundaryFinder.BoundaryReason.StartOfItem,
        end_of_item=QtCore.QTextBoundaryFinder.BoundaryReason.EndOfItem,
        mandatory_break=QtCore.QTextBoundaryFinder.BoundaryReason.MandatoryBreak,
        soft_hyphen=QtCore.QTextBoundaryFinder.BoundaryReason.SoftHyphen,
    )
)

BoundaryTypeStr = Literal[
    "grapheme",
    "word",
    "line",
    "sentence",
]

BOUNDARY_TYPES: bidict[BoundaryTypeStr, QtCore.QTextBoundaryFinder.BoundaryType] = bidict(
    grapheme=QtCore.QTextBoundaryFinder.BoundaryType.Grapheme,
    word=QtCore.QTextBoundaryFinder.BoundaryType.Word,
    line=QtCore.QTextBoundaryFinder.BoundaryType.Line,
    sentence=QtCore.QTextBoundaryFinder.BoundaryType.Sentence,
)


class TextBoundaryFinder(QtCore.QTextBoundaryFinder):
    """Way of finding Unicode text boundaries in a string."""

    def __init__(
        self,
        string_or_other: str | QtCore.QTextBoundaryFinder = "",
        boundary_type: (
            QtCore.QTextBoundaryFinder.BoundaryType | BoundaryTypeStr
        ) = "grapheme",
    ):
        if isinstance(string_or_other, QtCore.QTextBoundaryFinder):
            super().__init__(string_or_other)
        else:
            if isinstance(boundary_type, str):
                typ = BOUNDARY_TYPES[boundary_type]
            else:
                typ = boundary_type
            super().__init__(typ, string_or_other)

    def __repr__(self):
        return get_repr(self, self.string())

    def __reduce__(self):
        return type(self), (self.string(), self.type())

    def __iter__(self):
        pos = self.position()
        self.setPosition(0)
        p = 0
        # if self.isAtBoundary():
        #     yield 0
        while p != -1:
            p = self.toNextBoundary()
            if p != -1:
                yield p
        self.setPosition(pos)

    def get_boundary_type(self) -> BoundaryTypeStr:
        return BOUNDARY_TYPES.inverse[self.type()]

    def get_boundary_reasons(self) -> list[BoundaryReasonStr]:
        return BOUNDARY_REASONS.get_list(self.boundaryReasons())


if __name__ == "__main__":
    reg = TextBoundaryFinder("  This is a test", boundary_type="sentence")
    for p in reg:
        print(p)
