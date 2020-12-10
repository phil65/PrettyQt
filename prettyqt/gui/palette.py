from typing import Dict, Literal

from qtpy import QtGui

from prettyqt import gui, core
from prettyqt.utils import colors, bidict


ROLE = bidict(
    background=QtGui.QPalette.Background,  # same as Window
    foreground=QtGui.QPalette.Foreground,  # same as WindowText
    base=QtGui.QPalette.Base,
    alternate_base=QtGui.QPalette.AlternateBase,
    tool_tip_base=QtGui.QPalette.ToolTipBase,
    tool_tip_text=QtGui.QPalette.ToolTipText,
    placeholder_text=QtGui.QPalette.PlaceholderText,
    text=QtGui.QPalette.Text,
    button=QtGui.QPalette.Button,
    button_text=QtGui.QPalette.ButtonText,
    bright_text=QtGui.QPalette.BrightText,
)

RoleStr = Literal[
    "background",
    "foreground",
    "base",
    "alternate_base",
    "tool_tip_base",
    "tool_tip_text",
    "placeholder_text",
    "text",
    "button",
    "button_text",
    "bright_text",
]

GROUP = bidict(
    disabled=QtGui.QPalette.Disabled,
    active=QtGui.QPalette.Active,
    inactive=QtGui.QPalette.Inactive,
)

GroupStr = Literal["disabled", "active", "inactive"]


class Palette(QtGui.QPalette):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def __getitem__(self, index: RoleStr) -> gui.Color:
        return self.get_color(index)

    def __setitem__(self, index: RoleStr, value: colors.ColorType):
        self.set_color(index, value)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

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


if __name__ == "__main__":
    pal = Palette()
    print(pal.get_colors())
