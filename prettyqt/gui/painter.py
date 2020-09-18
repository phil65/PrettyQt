# -*- coding: utf-8 -*-

from typing import Union
import contextlib

from qtpy import QtCore, QtGui

from prettyqt import core, gui
from prettyqt.utils import bidict, colors, InvalidParamError


PEN_STYLES = gui.pen.PEN_STYLES  # type: ignore

JOIN_STYLES = gui.pen.JOIN_STYLES  # type: ignore

CAP_STYLES = gui.pen.CAP_STYLES  # type: ignore

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

CLIP_OPERATIONS = bidict(
    none=QtCore.Qt.NoClip,
    replace=QtCore.Qt.ReplaceClip,
    intersect=QtCore.Qt.IntersectClip,
)

RENDER_HINTS = bidict(
    antialiasing=QtGui.QPainter.Antialiasing,
    text_antialiasing=QtGui.QPainter.TextAntialiasing,
    smooth_pixmap_transform=QtGui.QPainter.SmoothPixmapTransform,
    high_quality_antialiasing=QtGui.QPainter.HighQualityAntialiasing,
    noncosmetic_default_pen=QtGui.QPainter.NonCosmeticDefaultPen,
    qt4_compatible_painting=QtGui.QPainter.Qt4CompatiblePainting,
    lossless_image_rendering=QtGui.QPainter.LosslessImageRendering,
)

FILL_RULES = bidict(odd_even=QtCore.Qt.OddEvenFill, winding=QtCore.Qt.WindingFill)


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

    def draw_image(
        self,
        target: Union[QtCore.QPoint, QtCore.QPointF, QtCore.QRect, QtCore.QRectF],
        frame_buffer: QtGui.QImage,
    ):
        self.set_composition_mode("source_atop")
        self.drawImage(target, frame_buffer)

    def draw_polygon(self, *args, fill_rule: str = "odd_even"):
        if fill_rule not in FILL_RULES:
            raise InvalidParamError(fill_rule, FILL_RULES)
        self.drawPolygon(*args, fillRule=FILL_RULES[fill_rule])

    def use_antialiasing(self):
        self.setRenderHint(self.Antialiasing, True)

    def fill_rect(
        self, rect: Union[QtCore.QRectF, QtCore.QRect], color, pattern: str = "solid"
    ):
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

    def set_pen(
        self,
        style: str = "solid",
        width: int = 1,
        color: colors.ColorType = "black",
        join_style: str = "bevel",
        cap_style: str = "square",
    ):
        """Set pen to use.

        Args:
            style: pen style to use
            width: pen width
            color: pen color
            join_style: pen join style to use
            cap_style: pen cap style to use
        """
        pen = gui.Pen()
        pen.set_style(style)
        pen.set_cap_style(cap_style)
        pen.set_join_style(join_style)
        pen.setWidth(width)
        pen.set_color(color)
        self.setPen(pen)

    def get_pen(self) -> str:
        """Return current pen.

        Returns:
            current pen
        """
        return gui.Pen(self.pen())

    def set_color(self, color: colors.ColorType):
        color = colors.get_color(color)
        self.setPen(color)

    def set_brush(self, brush: Union[QtGui.QBrush, colors.ColorType]):
        if not isinstance(brush, QtGui.QBrush):
            brush = colors.get_color(brush)
        self.setBrush(brush)

    def set_transparent_background(self, transparent: bool = True):
        mode = QtCore.Qt.TransparentMode if transparent else QtCore.Qt.OpaqueMode
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

    def set_clip_path(self, path: QtGui.QPainterPath, operation: str = "replace"):
        if operation not in CLIP_OPERATIONS:
            raise InvalidParamError(operation, CLIP_OPERATIONS)
        self.setClipPath(path, CLIP_OPERATIONS[operation])

    @contextlib.contextmanager
    def clip_path(self, operation: str = "replace"):
        path = gui.PainterPath()
        yield path
        self.set_clip_path(path, operation)
