from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


CursorPositionStr = Literal["cursor_between_characters", "cursor_on_character"]

CURSOR_POSITION: bidict[CursorPositionStr, QtGui.QTextLine.CursorPosition] = bidict(
    cursor_between_characters=QtGui.QTextLine.CursorPosition.CursorBetweenCharacters,
    cursor_on_character=QtGui.QTextLine.CursorPosition.CursorOnCharacter,
)

EdgeStr = Literal["leading", "trailing"]

EDGE: bidict[EdgeStr, QtGui.QTextLine.Edge] = bidict(
    leading=QtGui.QTextLine.Edge.Leading,
    trailing=QtGui.QTextLine.Edge.Trailing,
)


class TextLine(QtGui.QTextLine):
    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return get_repr(self)

    def __len__(self):
        return self.textLength()

    def get_position(self) -> core.PointF:
        return core.PointF(self.position())

    def set_position(self, point: datatypes.PointType):
        p = core.Point(*point) if isinstance(point, tuple) else point
        self.setPosition(p)

    def cursor_to_x(
        self, cursor_pos: int, edge: EdgeStr | QtGui.QTextLine.Edge = "leading"
    ) -> float:
        return self.cursorToX(cursor_pos, EDGE.get_enum_value(edge))  # type: ignore

    def x_to_cursor(
        self,
        x: float,
        cursor_pos: CursorPositionStr
        | QtGui.QTextLine.CursorPosition = "cursor_between_characters",
    ) -> int:
        return self.xToCursor(x, CURSOR_POSITION.get_enum_value(cursor_pos))


if __name__ == "__main__":
    fmt = TextLine()
