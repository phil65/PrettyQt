from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


SHAPE = bidict(
    line=QtWidgets.QRubberBand.Shape.Line, rectangle=QtWidgets.QRubberBand.Shape.Rectangle
)

ShapeStr = Literal["line", "rectangle"]


class RubberBandMixin(widgets.WidgetMixin):
    def __init__(
        self,
        shape: ShapeStr | QtWidgets.QRubberBand.Shape,
        parent: QtWidgets.QWidget | None = None,
        **kwargs,
    ):
        shape = SHAPE[shape] if isinstance(shape, str) else shape
        super().__init__(shape, parent, **kwargs)

    def get_shape(self) -> ShapeStr:
        return SHAPE.inverse[self.shape()]

    def track_widget(self, widget: QtWidgets.QWidget):
        from prettyqt import eventfilters

        event_catcher = eventfilters.EventCatcher(exclude="paint", parent=widget)
        widget.installEventFilter(event_catcher)
        event_catcher.caught.connect(self.update_size)

    def update_size(self):
        self.setGeometry(self.parent().rect())


class RubberBand(RubberBandMixin, QtWidgets.QRubberBand):
    pass


if __name__ == "__main__":
    app = widgets.app()
    splitter = widgets.Splitter()
    widget = widgets.RadioButton("test")
    widget2 = widgets.RadioButton("test")
    splitter.add(widget)
    splitter.add(widget2)
    rb = RubberBand("rectangle", widget)
    splitter.show()
    rb.track_widget(widget)
    rb.show()
    app.exec()
