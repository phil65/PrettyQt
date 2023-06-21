from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore


class OrientedScrollArea(widgets.ScrollArea):
    def __init__(
        self,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._orientation = orientation
        self.set_orientation(orientation)

    def orientation(self) -> QtCore.Qt.Orientation:
        """Get the orientation."""
        return self._orientation

    def set_orientation(self, orientation: QtCore.Qt.Orientation):
        """Set the orientation."""
        self._orientation = orientation
        if orientation == QtCore.Qt.Orientation.Horizontal:
            self.set_horizontal_scrollbar_policy("always_on")
            self.set_vertical_scrollbar_policy("always_off")
            self.set_size_policy("minimum_expanding", "fixed")
        else:
            self.set_horizontal_scrollbar_policy("always_off")
            self.set_vertical_scrollbar_policy("always_on")
            self.set_size_policy("fixed", "minimum_expanding")
        self.update()

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Filter events in order to get informed when the content widget resizes."""
        if obj == self.widget() and event.type() == QtCore.QEvent.Type.Resize:
            self.updateGeometry()
        return super().eventFilter(obj, event)

    def sizeHint(self) -> QtCore.QSize:
        """Determines the exact size along the axis orthogonal to the orientation."""
        widget = self.widget()
        if widget is None:
            return super().sizeHint()
        widget_size = widget.size()
        margins = self.contentsMargins()
        margins_width = margins.left() + margins.right()
        margins_height = margins.top() + margins.bottom()
        w = widget_size.width() + margins_width
        h = widget_size.height() + margins_height
        if self._orientation == QtCore.Qt.Orientation.Horizontal:
            return QtCore.QSize(w, h + self.horizontalScrollBar().sizeHint().height())
        else:  # self._orientation == Qt.Vertical:
            return QtCore.QSize(w + self.verticalScrollBar().sizeHint().width(), h)


if __name__ == "__main__":
    app = widgets.app()
    area = OrientedScrollArea()
    w = widgets.PlainTextEdit()
    # w.set_layout("horizontal")
    area.setWidget(w)
    # for i in range(100):
    #     w.box.addWidget(widgets.PlainTextEdit("test"))
    area.show()
    with app.debug_mode():
        app.exec()
