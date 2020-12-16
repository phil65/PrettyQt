from qtpy import QtGui, QtCore

from prettyqt import gui

from prettyqt.utils import bidict, InvalidParamError, mappers

FORMAT_TYPE = bidict(
    invalid=QtGui.QTextFormat.InvalidFormat,
    block=QtGui.QTextFormat.BlockFormat,
    char=QtGui.QTextFormat.CharFormat,
    list=QtGui.QTextFormat.ListFormat,
    frame=QtGui.QTextFormat.FrameFormat,
    user=QtGui.QTextFormat.UserFormat,
)

OBJECT_TYPE = bidict(
    none=QtGui.QTextFormat.NoObject,
    image=QtGui.QTextFormat.ImageObject,
    table=QtGui.QTextFormat.TableObject,
    table_cell=QtGui.QTextFormat.TableCellObject,
    user=QtGui.QTextFormat.UserObject,
)

PAGE_BREAK_FLAG = mappers.FlagMap(
    QtGui.QTextFormat.PageBreakFlags,
    auto=QtGui.QTextFormat.PageBreak_Auto,
    always_before=QtGui.QTextFormat.PageBreak_AlwaysBefore,
    always_after=QtGui.QTextFormat.PageBreak_AlwaysAfter,
)

LAYOUT_DIRECTIONS = bidict(
    left_to_right=QtCore.Qt.LeftToRight,
    right_to_left=QtCore.Qt.RightToLeft,
    auto=QtCore.Qt.LayoutDirectionAuto,
)


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

    def set_layout_direction(self, direction: str):
        """Set layout direction.

        Valid values: "left_to_right", "right_to_left", "auto"

        Args:
            direction: layout direction

        Raises:
            InvalidParamError: layout direction does not exist
        """
        if direction not in LAYOUT_DIRECTIONS:
            raise InvalidParamError(direction, LAYOUT_DIRECTIONS)
        self.setLayoutDirection(LAYOUT_DIRECTIONS[direction])

    def get_layout_direction(self) -> str:
        """Get the current layout direction.

        Possible values: "left_to_right", "right_to_left", "auto"

        Returns:
            layout direction
        """
        return LAYOUT_DIRECTIONS.inverse[self.layoutDirection()]


if __name__ == "__main__":
    fmt = TextFormat()
    print(bool(fmt))
