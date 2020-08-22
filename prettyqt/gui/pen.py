# -*- coding: utf-8 -*-

from qtpy import QtGui, QtCore

from prettyqt import core
from prettyqt.utils import colors
from prettyqt.utils import bidict, InvalidParamError

PEN_STYLES = bidict(
    none=QtCore.Qt.NoPen,
    solid=QtCore.Qt.SolidLine,
    dash=QtCore.Qt.DashLine,
    dot=QtCore.Qt.DotLine,
    dash_dot=QtCore.Qt.DashDotLine,
    dash_dot_dot=QtCore.Qt.DashDotDotLine,
    custom_dash=QtCore.Qt.CustomDashLine,
)

CAP_STYLES = bidict(
    flat=QtCore.Qt.FlatCap, square=QtCore.Qt.SquareCap, round=QtCore.Qt.RoundCap
)

JOIN_STYLES = bidict(
    miter=QtCore.Qt.MiterJoin,
    bevel=QtCore.Qt.BevelJoin,
    round=QtCore.Qt.RoundJoin,
    svg_miter=QtCore.Qt.SvgMiterJoin,
)


class Pen(QtGui.QPen):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def set_color(self, color: colors.ColorType):
        color = colors.get_color(color)
        self.setColor(color)

    def set_cap_style(self, style: str):
        """Set cap style to use.

        Allowed values are "flat", "square", "round"

        Args:
            style: cap style to use

        Raises:
            InvalidParamError: cap style does not exist
        """
        if style not in CAP_STYLES:
            raise InvalidParamError(style, CAP_STYLES)
        self.setCapStyle(CAP_STYLES[style])

    def get_cap_style(self) -> str:
        """Return current cap style.

        Possible values: "flat", "square", "round"

        Returns:
            cap style
        """
        return CAP_STYLES.inv[self.capStyle()]

    def set_join_style(self, style: str):
        """Set join style to use.

        Allowed values are "miter", "bevel", "round", "svg_miter"

        Args:
            style: join style to use

        Raises:
            InvalidParamError: join style does not exist
        """
        if style not in JOIN_STYLES:
            raise InvalidParamError(style, JOIN_STYLES)
        self.setJoinStyle(JOIN_STYLES[style])

    def get_join_style(self) -> str:
        """Return current join style.

        Possible values: "miter", "bevel", "round", "svg_miter"

        Returns:
            join style
        """
        return JOIN_STYLES.inv[self.joinStyle()]

    def set_style(self, style: str):
        """Set pen style to use.

        Allowed values are "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot",
        "custom_dash"

        Args:
            style: pen style to use

        Raises:
            InvalidParamError: pen style does not exist
        """
        if style not in PEN_STYLES:
            raise InvalidParamError(style, PEN_STYLES)
        self.setStyle(PEN_STYLES[style])

    def get_style(self) -> str:
        """Return current pen style.

        Possible values: "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot",
        "custom_dash"

        Returns:
            pen style
        """
        return PEN_STYLES.inv[self.style()]
