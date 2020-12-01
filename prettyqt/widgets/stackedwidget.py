# -*- coding: utf-8 -*-

from typing import Iterator

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStackedWidget.__bases__ = (widgets.Frame,)


class StackedWidget(QtWidgets.QStackedWidget):
    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.add(item)

    def __add__(self, other: QtWidgets.QWidget):
        if not isinstance(other, QtWidgets.QWidget):
            raise TypeError(f"Wrong type {other} for StackedWidget")
        self.addWidget(other)
        return self

    def __getitem__(self, index: int) -> QtWidgets.QWidget:
        return self.widget(index)

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.widget(i) for i in range(self.count()))

    def serialize_fields(self):
        return dict(items=list(self))

    def set_current_widget(self, widget):
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
