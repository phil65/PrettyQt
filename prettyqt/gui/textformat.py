from __future__ import annotations

from typing import Literal

import prettyqt
from prettyqt import constants, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, mappers


FORMAT_TYPE = bidict(
    invalid=QtGui.QTextFormat.FormatType.InvalidFormat,
    block=QtGui.QTextFormat.FormatType.BlockFormat,
    char=QtGui.QTextFormat.FormatType.CharFormat,
    list=QtGui.QTextFormat.FormatType.ListFormat,
    frame=QtGui.QTextFormat.FormatType.FrameFormat,
    user=QtGui.QTextFormat.FormatType.UserFormat,
)

FormatTypeStr = Literal["invalid", "block", "char", "list", "frame", "user"]

OBJECT_TYPE = bidict(
    none=QtGui.QTextFormat.ObjectTypes.NoObject,
    image=QtGui.QTextFormat.ObjectTypes.ImageObject,
    table=QtGui.QTextFormat.ObjectTypes.TableObject,
    table_cell=QtGui.QTextFormat.ObjectTypes.TableCellObject,
    user=QtGui.QTextFormat.ObjectTypes.UserObject,
)

ObjectTypeStr = Literal["none", "image", "table", "table_cell", "user"]

PAGE_BREAK_FLAG = mappers.FlagMap(
    QtGui.QTextFormat.PageBreakFlag,
    auto=QtGui.QTextFormat.PageBreakFlag.PageBreak_Auto,
    always_before=QtGui.QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore,
    always_after=QtGui.QTextFormat.PageBreakFlag.PageBreak_AlwaysAfter,
)

PageBreakFlagStr = Literal["auto", "always_before", "always_after"]


class TextFormat(QtGui.QTextFormat):
    def __getitem__(self, key: int):
        return self.property(key)

    def __setitem__(self, key: int, value):
        self.setProperty(key, value)

    def __contains__(self, key: int):
        return self.hasProperty(key)

    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return f"{type(self).__name__}({self.type()})"

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_brush_property(self, property_id: int) -> gui.Brush:
        return gui.Brush(self.brushProperty(property_id))

    def get_color_property(self, property_id: int) -> gui.Color:
        return gui.Color(self.colorProperty(property_id))

    def get_pen_property(self, property_id: int) -> gui.Pen:
        return gui.Pen(self.penProperty(property_id))

    def set_layout_direction(self, direction: constants.LayoutDirectionStr):
        """Set layout direction.

        Args:
            direction: layout direction

        Raises:
            InvalidParamError: layout direction does not exist
        """
        if direction not in constants.LAYOUT_DIRECTION:
            raise InvalidParamError(direction, constants.LAYOUT_DIRECTION)
        self.setLayoutDirection(constants.LAYOUT_DIRECTION[direction])

    def get_layout_direction(self) -> constants.LayoutDirectionStr:
        """Get the current layout direction.

        Returns:
            layout direction
        """
        return constants.LAYOUT_DIRECTION.inverse[self.layoutDirection()]

    def select_full_width(self, value: bool = True):
        if prettyqt.qt.API != "pyqt6":
            prop = QtGui.QTextFormat.FullWidthSelection
        else:
            prop = QtGui.QTextFormat.Property.FullWidthSelection  # type: ignore
        self.setProperty(prop, value)  # type: ignore


if __name__ == "__main__":
    fmt = TextFormat()
    print(bool(fmt))
