from typing import TYPE_CHECKING

from prettyqt import constants, core, widgets


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets

    _ScrollBarBase = QtWidgets.QScrollBar
else:
    _ScrollBarBase = object


class ScrollBarMixin(widgets.AbstractSliderMixin, _ScrollBarBase):
    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: constants.Orientation | constants.OrientationStr = "horizontal",
        parent: widgets.QWidget | None = None,
    ):
        ori = constants.ORIENTATION.get_enum_value(orientation)
        super().__init__(ori, parent)
        self.valueChanged.connect(self.on_value_change)

    @classmethod
    def setup_example(cls):
        w = widgets.ScrollArea()
        w.setVerticalScrollBar(cls(orientation="vertical", parent=w))
        return w

    def scroll_by_value(self, value: int):
        """Scroll by given distance."""
        value = min(max(self.minimum(), self.value() + value), self.maximum())
        self.setValue(value)

    def scroll_to(self, value: int):
        """Scroll to given position."""
        value = min(max(self.minimum(), value), self.maximum())
        self.setValue(value)

    def scroll_to_next_row(self):
        """Scroll to the next row."""
        self.setValue(self.value() + self.singleStep())

    def scroll_to_previous_row(self):
        """Scroll to the previous row."""
        self.setValue(self.value() - self.singleStep())

    def can_scroll(self) -> bool:
        return self.maximum() > 0


class ScrollBar(ScrollBarMixin, widgets.QScrollBar):
    """Vertical or horizontal scroll bar."""


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit("gfdgdf\n" * 1000)
    widget.show()
    app.exec()
