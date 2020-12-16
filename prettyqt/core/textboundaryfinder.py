from typing import List, Literal, Union

from qtpy import QtCore

from prettyqt.utils import bidict


BOUNDARY_REASONS = bidict(
    not_at_boundary=QtCore.QTextBoundaryFinder.NotAtBoundary,
    break_opportunity=QtCore.QTextBoundaryFinder.BreakOpportunity,
    start_of_item=QtCore.QTextBoundaryFinder.StartOfItem,
    end_of_item=QtCore.QTextBoundaryFinder.EndOfItem,
    mandatory_break=QtCore.QTextBoundaryFinder.MandatoryBreak,
    soft_hyphen=QtCore.QTextBoundaryFinder.SoftHyphen,
)

BoundaryReasonStr = Literal[
    "not_at_boundary",
    "break_opportunity",
    "start_of_item",
    "end_of_item",
    "mandatory_break",
    "soft_hyphen",
]

BOUNDARY_TYPES = bidict(
    grapheme=QtCore.QTextBoundaryFinder.Grapheme,
    word=QtCore.QTextBoundaryFinder.Word,
    line=QtCore.QTextBoundaryFinder.Line,
    sentence=QtCore.QTextBoundaryFinder.Sentence,
)

BoundaryTypeStr = Literal[
    "grapheme",
    "word",
    "line",
    "sentence",
]


class TextBoundaryFinder(QtCore.QTextBoundaryFinder):
    def __init__(
        self,
        string_or_other: Union[str, QtCore.QTextBoundaryFinder] = "",
        boundary_type: Union[int, BoundaryTypeStr] = BOUNDARY_TYPES["grapheme"],
    ):
        if isinstance(string_or_other, QtCore.QTextBoundaryFinder):
            super().__init__(string_or_other)
        else:
            if isinstance(boundary_type, str):
                boundary_type = BOUNDARY_TYPES[boundary_type]
            super().__init__(boundary_type, string_or_other)

    def __repr__(self):
        return f"{type(self).__name__}({self.string()!r})"

    def __reduce__(self):
        return self.__class__, (self.string(), int(self.type))

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

    def get_boundary_reasons(self) -> List[BoundaryReasonStr]:
        return [k for k, v in BOUNDARY_REASONS.items() if v & self.boundaryReasons()]


if __name__ == "__main__":
    reg = TextBoundaryFinder("  This is a test", boundary_type="sentence")
    for p in reg:
        print(p)
