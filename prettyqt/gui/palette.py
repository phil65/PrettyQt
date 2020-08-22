from qtpy import QtGui

from prettyqt import gui, core
from prettyqt.utils import colors, bidict


ROLES = bidict(
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

GROUPS = bidict(
    disabled=QtGui.QPalette.Disabled,
    active=QtGui.QPalette.Active,
    inactive=QtGui.QPalette.Inactive,
)


class Palette(QtGui.QPalette):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def __getitem__(self, index: str):
        return self.get_color(index)

    def __setitem__(self, index, value):
        self.set_color(index, value)

    def highlight_inactive(self):
        color = self.color(self.Active, self.Highlight)
        self.setColor(self.Inactive, self.Highlight, color)

    def set_color(self, role: str, color: colors.ColorType, group: str = "active"):
        color = colors.get_color(color)
        self.setColor(GROUPS[group], ROLES[role], color)

    def get_colors(self, group: str = "active"):
        return {k: self.get_color(k, group) for k in ROLES.keys()}

    def get_color(self, role: str, group: str = "active"):
        return gui.Color(self.color(GROUPS[group], ROLES[role]))


if __name__ == "__main__":
    pal = Palette()
    print(pal.get_colors())
