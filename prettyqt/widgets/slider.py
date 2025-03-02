from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import bidict


TickPositionStr = Literal["none", "both_sides", "above", "below"]

TICK_POSITION: bidict[TickPositionStr, widgets.QSlider.TickPosition] = bidict(
    none=widgets.QSlider.TickPosition.NoTicks,
    both_sides=widgets.QSlider.TickPosition.TicksBothSides,
    above=widgets.QSlider.TickPosition.TicksAbove,
    below=widgets.QSlider.TickPosition.TicksBelow,
)

TickPositionAllStr = Literal["none", "both_sides", "above", "below", "left", "right"]


class HollowHandleStyle(widgets.ProxyStyle):
    def __init__(self, config: dict | None = None):
        super().__init__()
        self.config = {
            "groove.height": 3,
            "sub-page.color": gui.Color(255, 255, 255),
            "add-page.color": gui.Color(255, 255, 255, 64),
            "handle.color": gui.Color(255, 255, 255),
            "handle.ring-width": 4,
            "handle.hollow-radius": 6,
            "handle.margin": 4,
        }
        config = config or {}
        self.config |= config

        # get handle size
        w = (
            self.config["handle.margin"]
            + self.config["handle.ring-width"]
            + self.config["handle.hollow-radius"]
        )
        self.config["handle.size"] = core.QSize(2 * w, 2 * w)

    def subControlRect(
        self,
        cc: widgets.QStyle.ComplexControl,
        opt: widgets.QStyleOptionSlider,
        sc: widgets.QStyle.SubControl,
        widget: widgets.QWidget,
    ):
        """Get the rectangular area occupied by the sub control."""
        if (
            cc != self.ComplexControl.CC_Slider
            or opt.orientation != constants.Orientation.Horizontal
            or sc == self.SubControl.SC_SliderTickmarks
        ):
            return super().subControlRect(cc, opt, sc, widget)

        rect = opt.rect

        if sc == self.SubControl.SC_SliderGroove:
            h = self.config["groove.height"]
            groove_rect = core.QRectF(0, (rect.height() - h) // 2, rect.width(), h)
            return groove_rect.toRect()

        if sc == self.SubControl.SC_SliderHandle:
            size = self.config["handle.size"]
            x = self.sliderPositionFromValue(
                opt.minimum, opt.maximum, opt.sliderPosition, rect.width()
            )

            # solve the situation that the handle runs out of slider
            x *= (rect.width() - size.width()) / rect.width()
            slider_rect = core.QRectF(x, 0, size.width(), size.height())
            return slider_rect.toRect()
        return None

    def drawComplexControl(
        self,
        cc: widgets.QStyle.ComplexControl,
        opt: widgets.QStyleOptionSlider,
        painter: gui.QPainter,
        widget: widgets.QWidget,
    ):
        """Draw sub control."""
        if (
            cc != self.ComplexControl.CC_Slider
            or opt.orientation != constants.Orientation.Horizontal
        ):
            return super().drawComplexControl(cc, opt, painter, widget)

        groove_rect = self.subControlRect(
            cc, opt, self.SubControl.SC_SliderGroove, widget
        )
        handle_rect = self.subControlRect(
            cc, opt, self.SubControl.SC_SliderHandle, widget
        )
        painter.setRenderHints(gui.Painter.RenderHint.Antialiasing)
        painter.setPen(constants.PenStyle.NoPen)

        # paint groove
        painter.save()
        painter.translate(groove_rect.topLeft())

        # paint the crossed part
        w = handle_rect.x() - groove_rect.x()
        h = self.config["groove.height"]
        painter.setBrush(self.config["sub-page.color"])
        painter.drawRect(0, 0, w, h)

        # paint the uncrossed part
        x = w + self.config["handle.size"].width()
        painter.setBrush(self.config["add-page.color"])
        painter.drawRect(x, 0, groove_rect.width() - w, h)
        painter.restore()

        # paint handle
        ring_width = self.config["handle.ring-width"]
        hollow_radius = self.config["handle.hollow-radius"]
        radius = ring_width + hollow_radius

        path = gui.PainterPath()
        path.moveTo(0, 0)
        center = handle_rect.center().toPointF() + core.QPointF(1, 1)
        path.addEllipse(center, radius, radius)
        path.addEllipse(center, hollow_radius, hollow_radius)

        handle_color = self.config["handle.color"]  # type:QColor
        handle_color.setAlpha(
            255 if opt.activeSubControls != self.SubControl.SC_SliderHandle else 153
        )
        painter.setBrush(handle_color)
        painter.drawPath(path)

        # press handle
        if widget.isSliderDown():
            handle_color.setAlpha(255)
            painter.setBrush(handle_color)
            painter.drawEllipse(handle_rect)
            return None
        return None


class Slider(widgets.AbstractSliderMixin, widgets.QSlider):
    """Vertical or horizontal slider."""

    value_changed = core.Signal(int)
    clicked = core.Signal(int)

    def __init__(self, *args, **kwargs):
        match args:
            case (str(), *rest):
                super().__init__(constants.ORIENTATION[args[0]], *rest, **kwargs)
            case _:
                super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.on_value_change)
        # style = HollowHandleStyle(
        #     {
        #         "groove.height": 4,
        #         "sub-page.color": gui.QColor(72, 210, 242),
        #         "add-page.color": gui.QColor(255, 255, 255, 50),
        #         "handle.color": gui.QColor(72, 210, 242),
        #         "handle.ring-width": 2,
        #         "handle.hollow-radius": 10,
        #         "handle.margin": 0,
        #     }
        # )
        # self.setStyle(style)

    def mousePressEvent(self, e: gui.QMouseEvent):
        self.clicked.emit(self.value())
        if self.orientation() == constants.Orientation.Horizontal:
            value = e.pos().x() / self.width() * self.maximum()
        else:
            value = (self.height() - e.pos().y()) / self.height() * self.maximum()

        self.setValue(int(value))
        super().mousePressEvent(e)

    def set_tick_position(
        self, position: TickPositionAllStr | widgets.QSlider.TickPosition
    ):
        """Set the tick position for the slider.

        For vertical orientation, "above" equals to "left" and "below" to "right".

        Args:
            position: position for the ticks
        """
        if position == "left":
            position = "above"
        elif position == "right":
            position = "below"
        self.setTickPosition(TICK_POSITION.get_enum_value(position))

    def get_tick_position(self) -> TickPositionStr:
        """Return tick position.

        Returns:
            tick position
        """
        return TICK_POSITION.inverse[self.tickPosition()]
        # if self.is_vertical():
        #     if val == "above":
        #         return "left"
        #     elif val == "below":
        #         return "right"


if __name__ == "__main__":
    app = widgets.app()
    slider = Slider()
    slider.setRange(0, 100)
    slider.show()
    app.exec()
