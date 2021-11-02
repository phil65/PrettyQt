from __future__ import annotations

from typing import Literal

from prettyqt import charts, core, gui, widgets
from prettyqt.qt import QtCharts, QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


RUBBER_BAND = bidict(
    none=QtCharts.QChartView.RubberBand.NoRubberBand,
    vertical=QtCharts.QChartView.RubberBand.VerticalRubberBand,
    horizontal=QtCharts.QChartView.RubberBand.HorizontalRubberBand,
    rectangle=QtCharts.QChartView.RubberBand.RectangleRubberBand,
)

RubberBandStr = Literal["none", "vertical", "horizontal", "rectangle"]


ZOOM_IN_FACTOR = 1.1
ZOOM_OUT_FACTOR = 1.0 / ZOOM_IN_FACTOR
SCROLL_STEP_SIZE = 10


class ChartView(QtCharts.QChartView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chart = charts.Chart()
        self.setChart(chart)
        self.setRenderHint(gui.Painter.RenderHint.Antialiasing)
        self.set_rubber_band("rectangle")
        # self.setDragMode(self.RubberBandDrag)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """Handle keypress events to allow navigation via keyboard."""
        key = event.key()
        if key == QtCore.Qt.Key.Key_Escape:
            self.chart().zoomReset()
        elif key == QtCore.Qt.Key.Key_Plus:
            self.chart().zoom_by_factor(ZOOM_IN_FACTOR)
        elif key == QtCore.Qt.Key.Key_Minus:
            self.chart().zoom_by_factor(ZOOM_OUT_FACTOR)
        elif key == QtCore.Qt.Key.Key_Left:
            self.chart().scroll(-SCROLL_STEP_SIZE, 0)
        elif key == QtCore.Qt.Key.Key_Right:
            self.chart().scroll(SCROLL_STEP_SIZE, 0)
        elif key == QtCore.Qt.Key.Key_Up:
            self.chart().scroll(0, SCROLL_STEP_SIZE)
        elif key == QtCore.Qt.Key.Key_Down:
            self.chart().scroll(0, -SCROLL_STEP_SIZE)
        elif key == QtCore.Qt.Key.Key_0:
            self.chart().apply_nice_numbers()
        else:
            super().keyPressEvent(event)
            return
        event.accept()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        """Handle wheel event for zooming."""
        fct = ZOOM_IN_FACTOR if event.angleDelta().y() > 0 else ZOOM_OUT_FACTOR
        self.chart().zoom_by_factor(fct)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Override to allow dragging the chart."""
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            widgets.Application.restoreOverrideCursor()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """Override to allow dragging the chart."""
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            cursor = gui.Cursor(QtCore.Qt.CursorShape.SizeAllCursor)
            widgets.Application.setOverrideCursor(cursor)
            self.last_mouse_pos = event.position()
            event.accept()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        """Override to allow dragging the chart."""
        # pan the chart with a middle mouse drag
        if event.buttons() & QtCore.Qt.MouseButton.RightButton:  # type: ignore
            if not self.last_mouse_pos:
                return
            pos_diff = event.position() - self.last_mouse_pos
            self.chart().scroll(-pos_diff.x(), pos_diff.y())

            self.last_mouse_pos = event.position()
            event.accept()

            widgets.Application.restoreOverrideCursor()

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

    def get_image(self) -> QtGui.QPixmap:
        image = self.grab()
        gl_widget = self.find_child(QtWidgets.QOpenGLWidget)
        if gl_widget:
            d = gl_widget.mapToGlobal(core.Point()) - self.mapToGlobal(core.Point())
            with gui.Painter(image) as painter:
                painter.set_composition_mode("source_atop")
                painter.drawImage(d, gl_widget.grabFramebuffer())
        return image

    def set_rubber_band(self, typ: RubberBandStr):
        """Set the rubber band type.

        Args:
            typ: rubber band type

        Raises:
            InvalidParamError: rubber band type does not exist
        """
        if typ not in RUBBER_BAND:
            raise InvalidParamError(typ, RUBBER_BAND)
        self.setRubberBand(RUBBER_BAND[typ])

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
    app.main_loop()
