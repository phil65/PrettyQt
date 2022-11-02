from __future__ import annotations

from collections.abc import Iterator
import contextlib
from typing import Literal

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict, colors, types


COMPOSITION_MODE = bidict(
    source_over=QtGui.QPainter.CompositionMode.CompositionMode_SourceOver,
    destination_over=QtGui.QPainter.CompositionMode.CompositionMode_DestinationOver,
    clear=QtGui.QPainter.CompositionMode.CompositionMode_Clear,
    source=QtGui.QPainter.CompositionMode.CompositionMode_Source,
    destination=QtGui.QPainter.CompositionMode.CompositionMode_Destination,
    source_in=QtGui.QPainter.CompositionMode.CompositionMode_SourceIn,
    destination_in=QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn,
    source_out=QtGui.QPainter.CompositionMode.CompositionMode_SourceOut,
    destination_out=QtGui.QPainter.CompositionMode.CompositionMode_DestinationOut,
    source_atop=QtGui.QPainter.CompositionMode.CompositionMode_SourceAtop,
    destination_atop=QtGui.QPainter.CompositionMode.CompositionMode_DestinationAtop,
)

CompositionModeStr = Literal[
    "source_over",
    "destination_over",
    "clear",
    "source",
    "destination",
    "source_in",
    "destination_in",
    "source_out",
    "destination_out",
    "source_atop",
    "destination_atop",
]

RENDER_HINTS = bidict(
    antialiasing=QtGui.QPainter.RenderHint.Antialiasing,
    text_antialiasing=QtGui.QPainter.RenderHint.TextAntialiasing,
    smooth_pixmap_transform=QtGui.QPainter.RenderHint.SmoothPixmapTransform,
    lossless_image_rendering=QtGui.QPainter.RenderHint.LosslessImageRendering,
)

RenderHintStr = Literal[
    "antialiasing",
    "text_antialiasing",
    "smooth_pixmap_transform",
    "lossless_image_rendering",
]


class Painter(QtGui.QPainter):
    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.end()

    @contextlib.contextmanager
    def paint_on(self, obj) -> Iterator[Painter]:
        self.begin(obj)
        yield self
        self.end()

    @contextlib.contextmanager
    def backup_state(self) -> Iterator[Painter]:
        self.save()
        yield self
        self.restore()

    @contextlib.contextmanager
    def native_mode(self) -> Iterator[Painter]:
        self.beginNativePainting()
        yield self
        self.endNativePainting()

    @contextlib.contextmanager
    def edit_pen(self) -> Iterator[gui.Pen]:
        pen = gui.Pen(self.pen())
        yield pen
        self.setPen(pen)

    def draw_image(
        self,
        target: QtCore.QPoint | QtCore.QPointF | QtCore.QRect | QtCore.QRectF,
        frame_buffer: QtGui.QImage,
    ):
        self.set_composition_mode("source_atop")
        self.drawImage(target, frame_buffer)

    def draw_polygon(
        self,
        points: (
            QtGui.QPolygon | QtGui.QPolygonF | list[QtCore.QPoint] | list[QtCore.QPointF]
        ),
        fill_rule: constants.FillRuleStr = "odd_even",
    ):
        if fill_rule not in constants.FILL_RULE:
            raise InvalidParamError(fill_rule, constants.FILL_RULE)
        self.drawPolygon(points, fillRule=constants.FILL_RULE[fill_rule])  # type: ignore

    def use_antialiasing(self):
        self.setRenderHint(self.RenderHint.Antialiasing, True)

    def fill_rect(
        self,
        rect: types.RectType | types.RectFType,
        color: types.ColorType,
        pattern: constants.PatternStr = "solid",
    ):
        if pattern not in constants.PATTERN:
            raise InvalidParamError(pattern, constants.PATTERN)
        if isinstance(rect, tuple):
            rect = core.RectF(*rect)
        color = colors.get_color(color)
        if pattern != "solid":
            color = gui.Brush(color, constants.PATTERN[pattern])
        self.fillRect(rect, color)

    def set_pen(
        self,
        style: constants.PenStyleStr | None = "solid",
        width: float = 1.0,
        color: types.ColorType = "black",
        brush: QtGui.QBrush | None = None,
        miter_limit: float = 2.0,
        join_style: constants.JoinStyleStr = "bevel",
        cap_style: constants.CapStyleStr = "square",
    ) -> gui.Pen:
        """Set pen to use.

        Args:
            style: pen style
            width: pen width
            color: pen color
            brush: pen brush
            miter_limit: miter limit
            join_style: pen join style
            cap_style: pen cap style
        """
        pen = gui.Pen()
        pen.set_style(style)
        if style in ["none", None]:
            self.setPen(pen)
            return pen
        pen.set_cap_style(cap_style)
        pen.set_join_style(join_style)
        pen.setMiterLimit(miter_limit)
        pen.setWidthF(width)
        if brush is not None:
            pen.setBrush(brush)
        pen.set_color(color)
        self.setPen(pen)
        return pen

    def get_pen(self) -> gui.Pen:
        """Return current pen.

        Returns:
            current pen
        """
        return gui.Pen(self.pen())

    def set_color(self, color: types.ColorType):
        color = colors.get_color(color)
        self.setPen(color)

    def set_brush(self, brush: QtGui.QBrush | types.ColorType):
        if not isinstance(brush, QtGui.QBrush):
            brush = colors.get_color(brush)
        self.setBrush(brush)

    def set_transparent_background(self, transparent: bool = True):
        mode = (
            QtCore.Qt.BGMode.TransparentMode
            if transparent
            else QtCore.Qt.BGMode.OpaqueMode
        )
        self.setBackgroundMode(mode)

    def set_composition_mode(self, mode: CompositionModeStr):
        """Set the current composition mode.

        Raises:
            InvalidParamError: composition mode does not exist
        """
        if mode not in COMPOSITION_MODE:
            raise InvalidParamError(mode, COMPOSITION_MODE)
        self.setCompositionMode(COMPOSITION_MODE[mode])

    def get_composition_mode(self) -> CompositionModeStr:
        """Get the current composition mode.

        Returns:
            composition mode
        """
        return COMPOSITION_MODE.inverse[self.compositionMode()]

    def get_font_metrics(self) -> gui.FontMetrics:
        return gui.FontMetrics(self.fontMetrics())

    def set_clip_path(
        self, path: QtGui.QPainterPath, operation: constants.ClipOperationStr = "replace"
    ):
        if operation not in constants.CLIP_OPERATION:
            raise InvalidParamError(operation, constants.CLIP_OPERATION)
        self.setClipPath(path, constants.CLIP_OPERATION[operation])

    def get_text_rect(self, text: str) -> core.Rect:
        return self.drawText(
            core.Rect(), QtCore.Qt.TextFlag.TextDontPrint, text
        )  # type: ignore

    @contextlib.contextmanager
    def clip_path(
        self, operation: constants.ClipOperationStr = "replace"
    ) -> Iterator[gui.PainterPath]:
        path = gui.PainterPath()
        yield path
        self.set_clip_path(path, operation)

    @contextlib.contextmanager
    def apply_transform(self, combine: bool = True) -> Iterator[gui.Transform]:
        transform = gui.Transform()
        yield transform
        self.setTransform(transform, combine)

    @contextlib.contextmanager
    def offset_by(self, x: int = 0, y: int = 0) -> Iterator[Painter]:
        self.translate(x, y)
        yield self
        self.translate(-x, -y)


if __name__ == "__main__":
    painter = Painter()
