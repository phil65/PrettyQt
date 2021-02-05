from __future__ import annotations

from prettyqt import constants, core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, colors, types


class Pen(QtGui.QPen):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __repr__(self):
        return f"{type(self).__name__}({self.get_color()})"

    def set_color(self, color: types.ColorType):
        color = colors.get_color(color)
        self.setColor(color)

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())

    def set_cap_style(self, style: constants.CapStyleStr):
        """Set cap style to use.

        Args:
            style: cap style to use

        Raises:
            InvalidParamError: cap style does not exist
        """
        if style not in constants.CAP_STYLE:
            raise InvalidParamError(style, constants.CAP_STYLE)
        self.setCapStyle(constants.CAP_STYLE[style])

    def get_cap_style(self) -> constants.CapStyleStr:
        """Return current cap style.

        Returns:
            cap style
        """
        return constants.CAP_STYLE.inverse[self.capStyle()]

    def set_join_style(self, style: constants.JoinStyleStr):
        """Set join style to use.

        Args:
            style: join style to use

        Raises:
            InvalidParamError: join style does not exist
        """
        if style not in constants.JOIN_STYLE:
            raise InvalidParamError(style, constants.JOIN_STYLE)
        self.setJoinStyle(constants.JOIN_STYLE[style])

    def get_join_style(self) -> constants.JoinStyleStr:
        """Return current join style.

        Returns:
            join style
        """
        return constants.JOIN_STYLE.inverse[self.joinStyle()]

    def set_style(self, style: constants.PenStyleStr | list[float] | None):
        """Set pen style to use.

        Args:
            style: pen style to use

        Raises:
            InvalidParamError: pen style does not exist
        """
        if isinstance(style, list):
            self.setDashPattern(style)
        else:
            if style is None:
                style = "none"
            if style not in constants.PEN_STYLE:
                raise InvalidParamError(style, constants.PEN_STYLE)
            self.setStyle(constants.PEN_STYLE[style])

    def get_style(self) -> constants.PenStyleStr:
        """Return current pen style.

        Returns:
            pen style
        """
        return constants.PEN_STYLE.inverse[self.style()]
