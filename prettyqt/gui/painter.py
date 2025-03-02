from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui
from prettyqt.utils import bidict, colors, datatypes


if TYPE_CHECKING:
    from collections.abc import Iterator


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

COMPOSITION_MODE: bidict[CompositionModeStr, gui.QPainter.CompositionMode] = bidict(
    source_over=gui.QPainter.CompositionMode.CompositionMode_SourceOver,
    destination_over=gui.QPainter.CompositionMode.CompositionMode_DestinationOver,
    clear=gui.QPainter.CompositionMode.CompositionMode_Clear,
    source=gui.QPainter.CompositionMode.CompositionMode_Source,
    destination=gui.QPainter.CompositionMode.CompositionMode_Destination,
    source_in=gui.QPainter.CompositionMode.CompositionMode_SourceIn,
    destination_in=gui.QPainter.CompositionMode.CompositionMode_DestinationIn,
    source_out=gui.QPainter.CompositionMode.CompositionMode_SourceOut,
    destination_out=gui.QPainter.CompositionMode.CompositionMode_DestinationOut,
    source_atop=gui.QPainter.CompositionMode.CompositionMode_SourceAtop,
    destination_atop=gui.QPainter.CompositionMode.CompositionMode_DestinationAtop,
)

RenderHintStr = Literal[
    "antialiasing",
    "text_antialiasing",
    "smooth_pixmap_transform",
    "lossless_image_rendering",
]

RENDER_HINTS: bidict[RenderHintStr, gui.QPainter.RenderHint] = bidict(
    antialiasing=gui.QPainter.RenderHint.Antialiasing,
    text_antialiasing=gui.QPainter.RenderHint.TextAntialiasing,
    smooth_pixmap_transform=gui.QPainter.RenderHint.SmoothPixmapTransform,
    lossless_image_rendering=gui.QPainter.RenderHint.LosslessImageRendering,
)


class PainterMixin:
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

    @contextlib.contextmanager
    def edit_font(self) -> Iterator[gui.Font]:
        font = gui.Font(self.font())
        yield font
        self.setFont(font)

    def draw_text(
        self,
        position: datatypes.PointType | datatypes.RectType | datatypes.RectFType,
        text: str,
        alignment: constants.AlignmentStr = "center",
    ):
        match position:
            case (_, _):
                position = core.Point(*position)
            case (_, _, _, _):
                position = core.RectF(*position)
        self.drawText(position, constants.ALIGNMENTS[alignment].value, text)

    def draw_image(
        self,
        target: core.QPoint | core.QPointF | core.QRect | core.QRectF,
        frame_buffer: gui.QImage,
    ):
        self.set_composition_mode("source_atop")
        self.drawImage(target, frame_buffer)

    def draw_polygon(
        self,
        points: gui.QPolygon | gui.QPolygonF | list[core.QPoint] | list[core.QPointF],
        fill_rule: constants.FillRuleStr | constants.FillRule = "odd_even",
    ):
        self.drawPolygon(points, fillRule=constants.FILL_RULE.get_enum_value(fill_rule))

    def draw_rounded_rect(
        self,
        rect: datatypes.RectType | datatypes.RectFType,
        x_radius: float,
        y_radius: float,
        relative: bool = False,
    ):
        flag = (
            constants.SizeMode.RelativeSize
            if relative
            else constants.SizeMode.AbsoluteSize
        )
        self.drawRoundedRect(datatypes.to_rect(rect), x_radius, y_radius, flag)

    def draw_star(self, size: float = 1.0, fill_rule: constants.FillRuleStr = "winding"):
        star = gui.PolygonF.create_star(size)
        self.drawPolygon(star, constants.FILL_RULE[fill_rule])

    def draw_diamond(
        self, size: float = 1.0, fill_rule: constants.FillRuleStr = "winding"
    ):
        star = gui.PolygonF.create_diamond(size)
        self.drawPolygon(star, constants.FILL_RULE[fill_rule])

    def use_antialiasing(self):
        self.setRenderHint(self.RenderHint.Antialiasing, True)

    def fill_rect(
        self,
        rect: datatypes.RectType | datatypes.RectFType,
        color: datatypes.ColorType,
        pattern: constants.BrushStyleStr | constants.BrushStyle = "solid",
    ):
        color = colors.get_color(color)
        if pattern != "solid":
            color = gui.Brush(color, constants.BRUSH_STYLE.get_enum_value(pattern))
        self.fillRect(datatypes.to_rect(rect), color)

    def set_pen(
        self,
        style: constants.PenStyleStr | None = "solid",
        width: float = 1.0,
        color: datatypes.ColorType = "black",
        brush: gui.QBrush | None = None,
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

    def set_color(self, color: datatypes.ColorType):
        color = colors.get_color(color)
        self.setPen(color)

    def set_brush(self, brush: gui.QBrush | datatypes.ColorType):
        if not isinstance(brush, gui.QBrush):
            brush = colors.get_color(brush)
        self.setBrush(brush)

    def set_transparent_background(self, transparent: bool = True):
        mode = (
            constants.BGMode.TransparentMode
            if transparent
            else constants.BGMode.OpaqueMode
        )
        self.setBackgroundMode(mode)

    def set_composition_mode(
        self, mode: CompositionModeStr | gui.QPainter.CompositionMode
    ):
        """Set the current composition mode.

        Arguments:
            mode: composition mode
        """
        self.setCompositionMode(COMPOSITION_MODE.get_enum_value(mode))

    def get_composition_mode(self) -> CompositionModeStr:
        """Get the current composition mode.

        Returns:
            composition mode
        """
        return COMPOSITION_MODE.inverse[self.compositionMode()]

    def set_transform(self, transform: datatypes.TransformType, combine: bool = False):
        self.setTransform(datatypes.to_transform(transform), combine)

    def get_font_metrics(self) -> gui.FontMetrics:
        return gui.FontMetrics(self.fontMetrics())

    def set_clip_path(
        self,
        path: gui.QPainterPath,
        operation: constants.ClipOperationStr | constants.ClipOperation = "replace",
    ):
        self.setClipPath(path, constants.CLIP_OPERATION.get_enum_value(operation))

    def get_text_rect(self, text: str) -> core.Rect:
        return self.drawText(core.Rect(), constants.TextFlag.TextDontPrint, text)  # type: ignore

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


class Painter(PainterMixin, gui.QPainter):
    """Performs low-level painting on widgets and other paint devices."""


if __name__ == "__main__":
    painter = Painter()
    painter.draw_text((0, 0, 1, 1), "aaa")
