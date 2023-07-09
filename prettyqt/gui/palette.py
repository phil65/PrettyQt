from __future__ import annotations

from typing import Literal

from typing_extensions import Self

from prettyqt import gui
from prettyqt.utils import bidict, colors, datatypes, get_repr, serializemixin


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


ROLE: bidict[RoleStr, gui.QPalette.ColorRole] = bidict(
    window=gui.QPalette.ColorRole.Window,  # same as Background
    window_text=gui.QPalette.ColorRole.WindowText,  # same as Foreground
    base=gui.QPalette.ColorRole.Base,
    alternate_base=gui.QPalette.ColorRole.AlternateBase,
    tool_tip_base=gui.QPalette.ColorRole.ToolTipBase,
    tool_tip_text=gui.QPalette.ColorRole.ToolTipText,
    placeholder_text=gui.QPalette.ColorRole.PlaceholderText,
    text=gui.QPalette.ColorRole.Text,
    button=gui.QPalette.ColorRole.Button,
    button_text=gui.QPalette.ColorRole.ButtonText,
    bright_text=gui.QPalette.ColorRole.BrightText,
    light=gui.QPalette.ColorRole.Light,
    midlight=gui.QPalette.ColorRole.Midlight,
    dark=gui.QPalette.ColorRole.Dark,
    mid=gui.QPalette.ColorRole.Mid,
    shadow=gui.QPalette.ColorRole.Shadow,
    highlight=gui.QPalette.ColorRole.Highlight,
    highlighted_text=gui.QPalette.ColorRole.HighlightedText,
    link=gui.QPalette.ColorRole.Link,
    link_visited=gui.QPalette.ColorRole.LinkVisited,
    none=gui.QPalette.ColorRole.NoRole,
)

GroupStr = Literal["disabled", "active", "inactive"]

GROUP: bidict[GroupStr, gui.QPalette.ColorGroup] = bidict(
    disabled=gui.QPalette.ColorGroup.Disabled,
    active=gui.QPalette.ColorGroup.Active,  # normal
    inactive=gui.QPalette.ColorGroup.Inactive,
)


class Palette(serializemixin.SerializeMixin, gui.QPalette):
    def __getitem__(self, index: RoleStr | gui.QPalette.ColorRole) -> gui.Color:
        return self.get_color(index)

    def __setitem__(
        self, index: RoleStr | gui.QPalette.ColorRole, value: datatypes.ColorType
    ):
        self.set_color(index, value)

    def __repr__(self):
        return get_repr(self, self.get_color("button"), self.get_color("window"))

    def yield_colors(
        self, mode: Literal["auto", "auto_inverted", "dark", "light"] = "auto"
    ):
        if mode == "auto":
            mode = "dark" if self.is_dark() else "light"
        elif mode == "auto_inverted":
            mode = "light" if self.is_dark() else "dark"
        for color in gui.Color.colorNames():
            c = gui.Color(color)
            if (c.is_dark() and mode == "dark") or (not c.is_dark() and mode == "light"):
                yield c.as_qt()

    def highlight_inactive(self, enable: bool = True):
        if enable:
            color = self.color(self.ColorGroup.Active, self.ColorRole.Highlight)
        else:
            pal = gui.Palette()
            color = pal.color(self.ColorGroup.Inactive, self.ColorRole.Highlight)
        self.setColor(self.ColorGroup.Inactive, self.ColorRole.Highlight, color)

    def set_color(
        self,
        role: RoleStr | gui.QPalette.ColorRole,
        color: datatypes.ColorType,
        group: GroupStr | gui.QPalette.ColorGroup = "active",
    ):
        color = colors.get_color(color)
        self.setColor(GROUP.get_enum_value(group), ROLE.get_enum_value(role), color)

    def get_colors(
        self, group: GroupStr | gui.QPalette.ColorGroup = "active"
    ) -> dict[str, gui.Color]:
        return {k: self.get_color(k, group) for k in ROLE}

    def get_color(
        self,
        role: RoleStr | gui.QPalette.ColorRole,
        group: GroupStr | gui.QPalette.ColorGroup = "active",
    ) -> gui.Color:
        return gui.Color(
            self.color(GROUP.get_enum_value(group), ROLE.get_enum_value(role))
        )

    def set_brush(
        self,
        role: RoleStr | gui.QPalette.ColorRole,
        brush: datatypes.ColorAndBrushType,
        group: GroupStr | gui.QPalette.ColorGroup = "active",
    ):
        if not isinstance(brush, gui.QBrush):
            brush = gui.Brush(colors.get_color(brush))
        self.setBrush(GROUP.get_enum_value(group), ROLE.get_enum_value(role), brush)

    def get_brushes(
        self, group: GroupStr | gui.QPalette.ColorGroup = "active"
    ) -> dict[str, gui.Brush]:
        return {k: self.get_brush(k, group) for k in ROLE}

    def get_brush(
        self,
        role: RoleStr | gui.QPalette.ColorRole,
        group: GroupStr | gui.QPalette.ColorGroup = "active",
    ) -> gui.Brush:
        return gui.Brush(
            self.brush(GROUP.get_enum_value(group), ROLE.get_enum_value(role))
        )

    def set_color_group(
        self, group: GroupStr | gui.QPalette.ColorGroup, **kwargs: gui.QBrush
    ):
        """Set the color group.

        Args:
            group: color group to use
            kwargs: keyword arguments passed to setColorGroup
        """
        self.setColorGroup(GROUP.get_enum_value(group), **kwargs)

    def get_color_group(self) -> GroupStr:
        """Return color group.

        Returns:
            color group
        """
        return GROUP.inverse[self.colorGroup()]

    def inverted(self) -> Self:
        pal = type(self)()
        for group in GROUP:
            for role in ROLE:
                color = self.get_color(role, group)
                pal.set_color(role, color.inverted(), group)
        return pal

    @classmethod
    def create_dark_palette(cls) -> Self:
        pal = cls()
        pal.set_color("window", gui.Color(53, 53, 53))
        pal.set_color("window_text", "white")
        pal.set_color("window_text", "grey", group="disabled")
        pal.set_color("base", gui.Color(25, 25, 25))
        pal.set_color("alternate_base", gui.Color(53, 53, 53))
        pal.set_color("tool_tip_base", "slategrey")
        pal.set_color("tool_tip_base", "slategrey", group="inactive")
        pal.set_color("tool_tip_text", "white")
        pal.set_color("tool_tip_text", "white", group="inactive")
        pal.set_color("text", "white")
        pal.set_color("text", "grey", group="disabled")
        pal.set_color("button", gui.Color(53, 53, 53))
        pal.set_color("button_text", "white")
        pal.set_color("button_text", "grey", group="disabled")
        pal.set_color("bright_text", "red")
        pal.set_color("link", "dodgerblue")
        pal.set_color("highlight", "dodgerblue")
        pal.set_color("highlight", gui.Color(80, 80, 80), group="disabled")
        pal.set_color("highlighted_text", "black")
        pal.set_color("highlighted_text", "grey", group="disabled")
        return pal

    def is_dark(self) -> bool:
        col = self.color(self.ColorRole.Window)
        return max(col.getRgb()[:3]) < 115


if __name__ == "__main__":
    pal = Palette()
    print(list(pal.yield_dark_colors()))
