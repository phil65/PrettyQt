from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui
from prettyqt.utils import bidict, get_repr


FORMAT_TYPE = bidict(
    invalid=gui.QTextFormat.FormatType.InvalidFormat,
    block=gui.QTextFormat.FormatType.BlockFormat,
    char=gui.QTextFormat.FormatType.CharFormat,
    list=gui.QTextFormat.FormatType.ListFormat,
    frame=gui.QTextFormat.FormatType.FrameFormat,
    user=gui.QTextFormat.FormatType.UserFormat,
)

FormatTypeStr = Literal["invalid", "block", "char", "list", "frame", "user"]

OBJECT_TYPE = bidict(
    none=gui.QTextFormat.ObjectTypes.NoObject,
    image=gui.QTextFormat.ObjectTypes.ImageObject,
    table=gui.QTextFormat.ObjectTypes.TableObject,
    table_cell=gui.QTextFormat.ObjectTypes.TableCellObject,
    user=gui.QTextFormat.ObjectTypes.UserObject,
)

ObjectTypeStr = Literal["none", "image", "table", "table_cell", "user"]

PAGE_BREAK_FLAG = bidict(
    auto=gui.QTextFormat.PageBreakFlag.PageBreak_Auto,
    always_before=gui.QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore,
    always_after=gui.QTextFormat.PageBreakFlag.PageBreak_AlwaysAfter,
)

PageBreakFlagStr = Literal["auto", "always_before", "always_after"]


class TextFormatMixin:
    def __getitem__(self, key: int):
        return self.property(key)

    def __setitem__(self, key: int, value):
        self.setProperty(key, value)

    def __contains__(self, key: int):
        return self.hasProperty(key)

    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return get_repr(self, self.type())

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

    def set_layout_direction(
        self, direction: constants.LayoutDirectionStr | constants.LayoutDirection
    ):
        """Set layout direction.

        Args:
            direction: layout direction
        """
        self.setLayoutDirection(constants.LAYOUT_DIRECTION.get_enum_value(direction))

    def get_layout_direction(self) -> constants.LayoutDirectionStr:
        """Get the current layout direction.

        Returns:
            layout direction
        """
        return constants.LAYOUT_DIRECTION.inverse[self.layoutDirection()]

    def select_full_width(self, value: bool = True):
        prop = gui.QTextFormat.Property.FullWidthSelection
        self.setProperty(prop, value)  # type: ignore


class TextFormat(TextFormatMixin, gui.QTextFormat):
    pass


if __name__ == "__main__":
    fmt = TextFormat()
