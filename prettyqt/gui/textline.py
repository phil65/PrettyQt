from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, types


CURSOR_POSITION = bidict(
    cursor_between_characters=QtGui.QTextLine.CursorPosition.CursorBetweenCharacters,
    cursor_on_character=QtGui.QTextLine.CursorPosition.CursorOnCharacter,
)

CursorPositionStr = Literal["cursor_between_characters", "cursor_on_character"]

EDGE = bidict(
    leading=QtGui.QTextLine.Edge.Leading,
    trailing=QtGui.QTextLine.Edge.Trailing,
)

EdgeStr = Literal["leading", "trailing"]


class TextLine(QtGui.QTextLine):
    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __len__(self):
        return self.textLength()

    def get_position(self) -> core.Point:
        return core.Point(self.position())

    def set_position(self, point: types.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setPosition(point)

    def cursor_to_x(self, cursor_pos: int, edge: EdgeStr = "leading") -> float:
        if edge not in EDGE:
            raise InvalidParamError(edge, EDGE)
        return self.cursorToX(cursor_pos, EDGE[edge])  # type: ignore

    def x_to_cursor(
        self, x: float, cursor_pos: CursorPositionStr = "cursor_between_characters"
    ) -> int:
        if cursor_pos not in CURSOR_POSITION:
            raise InvalidParamError(cursor_pos, CURSOR_POSITION)
        return self.xToCursor(x, CURSOR_POSITION[cursor_pos])


if __name__ == "__main__":
    fmt = TextLine()
    print(bool(fmt))
