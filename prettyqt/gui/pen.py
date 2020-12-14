from typing import Literal

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import colors
from prettyqt.utils import bidict, InvalidParamError

PEN_STYLE = bidict(
    none=QtCore.Qt.NoPen,
    solid=QtCore.Qt.SolidLine,
    dash=QtCore.Qt.DashLine,
    dot=QtCore.Qt.DotLine,
    dash_dot=QtCore.Qt.DashDotLine,
    dash_dot_dot=QtCore.Qt.DashDotDotLine,
    custom_dash=QtCore.Qt.CustomDashLine,
)

PenStyleStr = Literal[
    "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot", "custom_dash"
]

CAP_STYLE = bidict(
    flat=QtCore.Qt.FlatCap, square=QtCore.Qt.SquareCap, round=QtCore.Qt.RoundCap
)

CapStyleStr = Literal["flat", "square", "round"]

JOIN_STYLE = bidict(
    miter=QtCore.Qt.MiterJoin,
    bevel=QtCore.Qt.BevelJoin,
    round=QtCore.Qt.RoundJoin,
    svg_miter=QtCore.Qt.SvgMiterJoin,
)

JoinStyleStr = Literal["miter", "bevel", "round" "svg_miter"]


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

    def set_color(self, color: colors.ColorType):
        color = colors.get_color(color)
        self.setColor(color)

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())

    def set_cap_style(self, style: CapStyleStr):
        """Set cap style to use.

        Allowed values are "flat", "square", "round"

        Args:
            style: cap style to use

        Raises:
            InvalidParamError: cap style does not exist
        """
        if style not in CAP_STYLE:
            raise InvalidParamError(style, CAP_STYLE)
        self.setCapStyle(CAP_STYLE[style])

    def get_cap_style(self) -> CapStyleStr:
        """Return current cap style.

        Possible values: "flat", "square", "round"

        Returns:
            cap style
        """
        return CAP_STYLE.inverse[self.capStyle()]

    def set_join_style(self, style: JoinStyleStr):
        """Set join style to use.

        Allowed values are "miter", "bevel", "round", "svg_miter"

        Args:
            style: join style to use

        Raises:
            InvalidParamError: join style does not exist
        """
        if style not in JOIN_STYLE:
            raise InvalidParamError(style, JOIN_STYLE)
        self.setJoinStyle(JOIN_STYLE[style])

    def get_join_style(self) -> JoinStyleStr:
        """Return current join style.

        Possible values: "miter", "bevel", "round", "svg_miter"

        Returns:
            join style
        """
        return JOIN_STYLE.inverse[self.joinStyle()]

    def set_style(self, style: str):
        """Set pen style to use.

        Allowed values are "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot",
        "custom_dash"

        Args:
            style: pen style to use

        Raises:
            InvalidParamError: pen style does not exist
        """
        if style not in PEN_STYLE:
            raise InvalidParamError(style, PEN_STYLE)
        self.setStyle(PEN_STYLE[style])

    def get_style(self) -> str:
        """Return current pen style.

        Possible values: "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot",
        "custom_dash"

        Returns:
            pen style
        """
        return PEN_STYLE.inverse[self.style()]
