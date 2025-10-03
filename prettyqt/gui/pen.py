from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import constants, gui
from prettyqt.utils import colors, get_repr, serializemixin


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class Pen(serializemixin.SerializeMixin, gui.QPen):
    """Defines how a QPainter should draw lines and outlines of shapes."""

    def __repr__(self):
        return get_repr(self, self.get_color())

    def set_color(self, color: datatypes.ColorType):
        color = colors.get_color(color)
        self.setColor(color)

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())

    def set_cap_style(self, style: constants.CapStyleStr | constants.PenCapStyle):
        """Set cap style to use.

        Args:
            style: cap style to use
        """
        self.setCapStyle(constants.CAP_STYLE.get_enum_value(style))

    def get_cap_style(self) -> constants.CapStyleStr:
        """Return current cap style.

        Returns:
            cap style
        """
        return constants.CAP_STYLE.inverse[self.capStyle()]

    def set_join_style(self, style: constants.JoinStyleStr | constants.PenJoinStyle):
        """Set join style to use.

        Args:
            style: join style to use
        """
        self.setJoinStyle(constants.JOIN_STYLE.get_enum_value(style))

    def get_join_style(self) -> constants.JoinStyleStr:
        """Return current join style.

        Returns:
            join style
        """
        return constants.JOIN_STYLE.inverse[self.joinStyle()]

    def set_style(
        self, style: constants.PenStyleStr | constants.PenStyle | list[float] | None
    ):
        """Set pen style to use.

        Args:
            style: pen style to use
        """
        if isinstance(style, list):
            self.setDashPattern(style)
        else:
            if style is None:
                style = "none"
            self.setStyle(constants.PEN_STYLE.get_enum_value(style))

    def get_style(self) -> constants.PenStyleStr:
        """Return current pen style.

        Returns:
            pen style
        """
        return constants.PEN_STYLE.inverse[self.style()]
