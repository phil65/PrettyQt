from qtpy.QtCharts import QtCharts
from qtpy import QtCore

from prettyqt import widgets, gui
from prettyqt.utils import bidict, InvalidParamError


MARKER_SHAPES = bidict(
    default=QtCharts.QLegend.MarkerShapeDefault,
    rectangle=QtCharts.QLegend.MarkerShapeRectangle,
    circle=QtCharts.QLegend.MarkerShapeCircle,
    from_series=QtCharts.QLegend.MarkerShapeFromSeries,
)

ALIGNMENTS = bidict(
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
)

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

    def set_alignment(self, alignment: str):
        """Set the alignment of the legend.

        Allowed values are "left", "right", "top", "bottom"

        Args:
            alignment: alignment for the legend

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in ALIGNMENTS:
            raise InvalidParamError(alignment, ALIGNMENTS)
        self.setAlignment(ALIGNMENTS[alignment])

    def get_alignment(self) -> str:
        """Return current alignment.

        Possible values: "left", "right", "top", "bottom"

        Returns:
            alignment
        """
        return ALIGNMENTS.inverse[self.alignment()]

    def set_marker_shape(self, shape: str):
        """Set the marker shape.

        Allowed values are "default", "rectangle", "circle", "from_series"

        Args:
            shape: marker shape

        Raises:
            InvalidParamError: marker shape does not exist
        """
        if shape not in MARKER_SHAPES:
            raise InvalidParamError(shape, MARKER_SHAPES)
        self.setMarkerShape(MARKER_SHAPES[shape])

    def get_marker_shape(self) -> str:
        """Return current marker shape.

        Possible values are "default", "rectangle", "circle", "from_series"

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
