from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtCharts
from prettyqt.utils import InvalidParamError, bidict


MARKER_SHAPES = bidict(
    default=QtCharts.QLegend.MarkerShape.MarkerShapeDefault,
    rectangle=QtCharts.QLegend.MarkerShape.MarkerShapeRectangle,
    circle=QtCharts.QLegend.MarkerShape.MarkerShapeCircle,
    from_series=QtCharts.QLegend.MarkerShape.MarkerShapeFromSeries,
)

MarkerShapeStr = Literal["default", "rectangle", "circle", "from_series"]

QtCharts.QLegend.__bases__ = (widgets.GraphicsWidget,)


class Legend:
    def __init__(self, item: QtCharts.QLegend):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def serialize_fields(self):
        return dict(
            alignment=self.get_alignment(),
            background_visible=self.isBackgroundVisible(),
            border_color=self.get_border_color(),
            color=self.get_color(),
            font=self.get_font(),
            label_color=self.get_label_color(),
            marker_shape=self.get_marker_shape(),
            reverse_markers=self.reverseMarkers(),
            show_tooltips=self.showToolTips(),
        )

    def set_alignment(self, alignment: constants.SideStr):
        """Set the alignment of the legend.

        Args:
            alignment: alignment for the legend

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.SIDES:
            raise InvalidParamError(alignment, constants.SIDES)
        self.setAlignment(constants.SIDES[alignment])

    def get_alignment(self) -> constants.SideStr:
        """Return current alignment.

        Returns:
            alignment
        """
        return constants.SIDES.inverse[self.alignment()]

    def set_marker_shape(self, shape: MarkerShapeStr):
        """Set the marker shape.

        Args:
            shape: marker shape

        Raises:
            InvalidParamError: marker shape does not exist
        """
        if shape not in MARKER_SHAPES:
            raise InvalidParamError(shape, MARKER_SHAPES)
        self.setMarkerShape(MARKER_SHAPES[shape])

    def get_marker_shape(self) -> MarkerShapeStr:
        """Return current marker shape.

        Returns:
            Marker shape
        """
        return MARKER_SHAPES.inverse[self.markerShape()]

    def get_border_color(self) -> gui.Color:
        return gui.Color(self.borderColor())

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_label_color(self) -> gui.Color:
        return gui.Color(self.labelColor())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())
