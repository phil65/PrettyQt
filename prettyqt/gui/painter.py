# -*- coding: utf-8 -*-

from typing import Union
import contextlib

from qtpy import QtCore, QtGui

from prettyqt import core, gui
from prettyqt.utils import bidict, colors, InvalidParamError


PEN_TYPES = bidict(none=QtCore.Qt.NoPen)

COMP_MODES = bidict(
    source_over=QtGui.QPainter.CompositionMode_SourceOver,
    destination_over=QtGui.QPainter.CompositionMode_DestinationOver,
    clear=QtGui.QPainter.CompositionMode_Clear,
    source=QtGui.QPainter.CompositionMode_Source,
    destination=QtGui.QPainter.CompositionMode_Destination,
    source_in=QtGui.QPainter.CompositionMode_SourceIn,
    destination_in=QtGui.QPainter.CompositionMode_DestinationIn,
    source_out=QtGui.QPainter.CompositionMode_SourceOut,
    destination_out=QtGui.QPainter.CompositionMode_DestinationOut,
    source_atop=QtGui.QPainter.CompositionMode_SourceAtop,
    destination_atop=QtGui.QPainter.CompositionMode_DestinationAtop,
)

PATTERNS = bidict(
    solid=QtCore.Qt.SolidPattern,
    none=QtCore.Qt.NoBrush,
    cross=QtCore.Qt.CrossPattern,
    linear_gradient=QtCore.Qt.LinearGradientPattern,
    radial_gradient=QtCore.Qt.RadialGradientPattern,
)


class Painter(QtGui.QPainter):
    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.end()

    @contextlib.contextmanager
    def paint_on(self, obj):
        self.begin(obj)
        yield self
        self.end()

    def draw_image(self, point, frame_buffer):
        self.set_composition_mode("source_atop")
        self.drawImage(point, frame_buffer)

    def use_antialiasing(self):
        self.setRenderHint(self.Antialiasing, True)

    def fill_rect(self, rect, color, pattern="solid"):
        if pattern not in PATTERNS:
            raise InvalidParamError(pattern, PATTERNS)
        if isinstance(rect, tuple):
            rect = core.Rect(*rect)
        if isinstance(color, str):
            if color not in gui.Color.colorNames():
                raise ValueError("Invalid value for color.")
            color = gui.Color(color)
        if pattern != "solid":
            color = gui.Brush(color, PATTERNS[pattern])
        self.fillRect(rect, color)

    def set_pen(self, pen_type: str):
        """Set pen type to use.

        Allowed values are "none",

        Args:
            pen_type: pen type to use

        Raises:
            InvalidParamError: pen type does not exist
        """
        if pen_type not in PEN_TYPES:
            raise InvalidParamError(pen_type, PEN_TYPES)
        self.setPen(PEN_TYPES[pen_type])

    def get_pen(self) -> str:
        """Return current pen type.

        Possible values: "none",

        Returns:
            pen type
        """
        return PEN_TYPES.inv[self.pen()]

    def set_color(self, color: colors.ColorType):
        color = colors.get_color(color)
        self.setPen(color)

    def set_brush(self, brush: Union[QtGui.QBrush, colors.ColorType]):
        if not isinstance(brush, QtGui.QBrush):
            brush = colors.get_color(brush)
        self.setBrush(brush)

    def set_transparent_background(self, transparent: bool = True):
        if transparent:
            mode = QtCore.Qt.TransparentMode
        else:
            mode = QtCore.Qt.OpaqueMode
        self.setBackgroundMode(mode)

    def set_composition_mode(self, mode: str):
        """Set the current composition mode.

        Possible values: "source_over", "destination_over", "clear", "source",
                         "destination", "source_in", "destination_in", "source_out",
                         "destination_out", "source_atop", "destination_atop",

        Raises:
            InvalidParamError: composition mode does not exist
        """
        if mode not in COMP_MODES:
            raise InvalidParamError(mode, COMP_MODES)
        self.setCompositionMode(COMP_MODES[mode])

    def get_composition_mode(self) -> str:
        """Get the current composition mode.

        Possible values: "source_over", "destination_over", "clear", "source",
                         "destination", "source_in", "destination_in", "source_out",
                         "destination_out", "source_atop", "destination_atop",

        Returns:
            composition mode
        """
        return COMP_MODES.inv[self.compositionMode()]

    def draw_text(self, x, y, text):
        self.drawText(x, y, text)
