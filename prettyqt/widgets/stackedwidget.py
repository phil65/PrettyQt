from __future__ import annotations

from collections.abc import Iterator

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStackedWidget.__bases__ = (widgets.Frame,)


class StackedWidget(QtWidgets.QStackedWidget):
    def __setstate__(self, state):
        for item in state["items"]:
            self.add(item)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: QtWidgets.QWidget) -> StackedWidget:
        self.addWidget(other)
        return self

    def __getitem__(self, index: int) -> QtWidgets.QWidget:
        return self.widget(index)

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.widget(i) for i in range(self.count()))

    def __len__(self):
        # needed for PySide2
        return self.count()

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

    def serialize_fields(self):
        return dict(items=list(self))

    def set_current_widget(self, widget: QtWidgets.QWidget):
        self.setCurrentWidget(widget)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    stackedwidget = StackedWidget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.RadioButton("Test 2")
    stackedwidget += widget2
    stackedwidget += widget3
    stackedwidget.show()
    app.main_loop()
