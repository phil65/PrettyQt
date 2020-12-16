from typing import Dict, Literal

from qtpy import QtGui

from prettyqt import core, gui
from prettyqt.utils import InvalidParamError, bidict, colors


ROLE = bidict(
    window=QtGui.QPalette.Window,  # same as Background
    window_text=QtGui.QPalette.WindowText,  # same as Foreground
    base=QtGui.QPalette.Base,
    alternate_base=QtGui.QPalette.AlternateBase,
    tool_tip_base=QtGui.QPalette.ToolTipBase,
    tool_tip_text=QtGui.QPalette.ToolTipText,
    placeholder_text=QtGui.QPalette.PlaceholderText,
    text=QtGui.QPalette.Text,
    button=QtGui.QPalette.Button,
    button_text=QtGui.QPalette.ButtonText,
    bright_text=QtGui.QPalette.BrightText,
    light=QtGui.QPalette.Light,
    midlight=QtGui.QPalette.Midlight,
    dark=QtGui.QPalette.Dark,
    mid=QtGui.QPalette.Mid,
    shadow=QtGui.QPalette.Shadow,
    highlight=QtGui.QPalette.Highlight,
    highlighted_text=QtGui.QPalette.HighlightedText,
    link=QtGui.QPalette.Link,
    link_visited=QtGui.QPalette.LinkVisited,
    none=QtGui.QPalette.NoRole,
)

RoleStr = Literal[
    "window",
    "window_text",
    "base",
    "alternate_base",
    "tool_tip_base",
    "tool_tip_text",
    "placeholder_text",
    "text",
    "button",
    "button_text",
    "bright_text",
    "light",
    "midlight",
    "dark",
    "mid",
    "shadow",
    "highlight",
    "highlighted_text",
    "link",
    "link_visited",
    "none",
]

GROUP = bidict(
    disabled=QtGui.QPalette.Disabled,
    active=QtGui.QPalette.Active,
    inactive=QtGui.QPalette.Inactive,
)

GroupStr = Literal["disabled", "active", "inactive"]


class Palette(QtGui.QPalette):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getitem__(self, index: RoleStr) -> gui.Color:
        return self.get_color(index)

    def __setitem__(self, index: RoleStr, value: colors.ColorType):
        self.set_color(index, value)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __repr__(self):
        return f"{type(self).__name__}({self['button']}, {self['window']})"

    def highlight_inactive(self):
        color = self.color(self.Active, self.Highlight)
        self.setColor(self.Inactive, self.Highlight, color)

    def set_color(
        self, role: RoleStr, color: colors.ColorType, group: GroupStr = "active"
    ):
        color = colors.get_color(color)
        self.setColor(GROUP[group], ROLE[role], color)

    def get_colors(self, group: GroupStr = "active") -> Dict[str, gui.Color]:
        return {k: self.get_color(k, group) for k in ROLE.keys()}

    def get_color(self, role: RoleStr, group: GroupStr = "active") -> gui.Color:
        return gui.Color(self.color(GROUP[group], ROLE[role]))

    def set_brush(
        self, role: RoleStr, brush: colors.ColorAndBrushType, group: GroupStr = "active"
    ):
        if not isinstance(brush, QtGui.QBrush):
            brush = gui.Brush(colors.get_color(brush))
        self.setBrush(GROUP[group], ROLE[role], brush)

    def get_brushes(self, group: GroupStr = "active") -> Dict[str, gui.Brush]:
        return {k: self.get_brush(k, group) for k in ROLE.keys()}

    def get_brush(self, role: RoleStr, group: GroupStr = "active") -> gui.Brush:
        return gui.Brush(self.brush(GROUP[group], ROLE[role]))

    def set_color_group(self, group: GroupStr):
        """Set the color group.

        Args:
            group: color group to use

        Raises:
            InvalidParamError: invalid color group
        """
        if group not in GROUP:
            raise InvalidParamError(group, GROUP)
        self.setColorGroup(GROUP[group])

    def get_color_group(self) -> GroupStr:
        """Return color group.

        Returns:
            color group
        """
        return GROUP.inverse[self.colorGroup()]


if __name__ == "__main__":
    pal = Palette()
    print(pal.get_colors())
