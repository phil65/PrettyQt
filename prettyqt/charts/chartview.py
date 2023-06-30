from __future__ import annotations

from typing import Literal

from prettyqt import charts, constants, core, gui, widgets
from prettyqt.utils import bidict


RubberBandStr = Literal["none", "vertical", "horizontal", "rectangle"]

RUBBER_BAND: bidict[RubberBandStr, charts.QChartView.RubberBand] = bidict(
    none=charts.QChartView.RubberBand.NoRubberBand,
    vertical=charts.QChartView.RubberBand.VerticalRubberBand,
    horizontal=charts.QChartView.RubberBand.HorizontalRubberBand,
    rectangle=charts.QChartView.RubberBand.RectangleRubberBand,
)

ZOOM_IN_FACTOR = 1.1
ZOOM_OUT_FACTOR = 1.0 / ZOOM_IN_FACTOR
SCROLL_STEP_SIZE = 10


class ChartView(widgets.GraphicsViewMixin, charts.QChartView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not args or not isinstance(args[0], charts.QChart):
            self.setChart(charts.Chart())
        self.setRenderHint(gui.Painter.RenderHint.Antialiasing)
        self.set_rubber_band("rectangle")
        # self.setDragMode(self.RubberBandDrag)

    def keyPressEvent(self, event: gui.QKeyEvent):
        """Handle keypress events to allow navigation via keyboard."""
        match event.key():
            case constants.Key.Key_Escape:
                self.chart().zoomReset()
            case constants.Key.Key_Plus:
                self.chart().zoom_by_factor(ZOOM_IN_FACTOR)
            case constants.Key.Key_Minus:
                self.chart().zoom_by_factor(ZOOM_OUT_FACTOR)
            case constants.Key.Key_Left:
                self.chart().scroll(-SCROLL_STEP_SIZE, 0)
            case constants.Key.Key_Right:
                self.chart().scroll(SCROLL_STEP_SIZE, 0)
            case constants.Key.Key_Up:
                self.chart().scroll(0, SCROLL_STEP_SIZE)
            case constants.Key.Key_Down:
                self.chart().scroll(0, -SCROLL_STEP_SIZE)
            case constants.Key.Key_0:
                self.chart().apply_nice_numbers()
            case _:
                super().keyPressEvent(event)
                return
        event.accept()

    def wheelEvent(self, event: gui.QWheelEvent):
        """Handle wheel event for zooming."""
        fct = ZOOM_IN_FACTOR if event.angleDelta().y() > 0 else ZOOM_OUT_FACTOR
        self.chart().zoom_by_factor(fct)
        event.accept()

    def mouseReleaseEvent(self, event: gui.QMouseEvent):
        """Override to allow dragging the chart."""
        if event.button() == constants.MouseButton.RightButton:
            widgets.Application.restoreOverrideCursor()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event: gui.QMouseEvent):
        """Override to allow dragging the chart."""
        if event.button() == constants.MouseButton.RightButton:
            widgets.Application.set_override_cursor("size_all")
            self.last_mouse_pos = event.position()
            event.accept()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: gui.QMouseEvent):
        """Override to allow dragging the chart."""
        # pan the chart with a middle mouse drag
        if event.buttons() & constants.MouseButton.RightButton:  # type: ignore
            if not self.last_mouse_pos:
                return
            pos_diff = event.position() - self.last_mouse_pos
            self.chart().scroll(-pos_diff.x(), pos_diff.y())

            self.last_mouse_pos = event.position()
            event.accept()

        super().mouseMoveEvent(event)

    @core.Slot()
    def save_as_image(self):
        """Let user choose folder and save chart as an image file."""
        dlg = widgets.FileDialog(mode="save", caption="Save image")
        filters = {"Bmp files": [".bmp"], "Jpeg files": [".jpg"], "Png files": [".png"]}
        dlg.set_extension_filter(filters)
        filename = dlg.open_file()
        if not filename:
            return
        self.chart().show_legend()
        image = self.get_image()
        image.save(str(filename[0]))
        self.chart().hide_legend()

    def set_rubber_band(self, typ: RubberBandStr | charts.QChartView.RubberBand):
        """Set the rubber band type.

        Args:
            typ: rubber band type
        """
        self.setRubberBand(RUBBER_BAND.get_enum_value(typ))

    def get_rubber_band(self) -> RubberBandStr:
        """Return current rubber band type.

        Returns:
            Rubber band type
        """
        return RUBBER_BAND.inverse[self.rubberBand()]

    # def hide_legend(self):
    #     self.chart().hide_legend()

    # def show_legend(self):
    #     self.chart().show_legend()

    # def set_legend_alignment(self, alignment: str):
    #     if alignment not in constants.SIDES:
    #         raise ValueError(f"{alignment!r} not a valid alignment.")
    #     self.chart().legend().setAlignment(constants.SIDES[alignment])


if __name__ == "__main__":
    app = widgets.app()
    widget = ChartView()
    widget.show()
    app.exec()
