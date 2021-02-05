from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStackedLayout.__bases__ = (widgets.Layout,)


class StackedLayout(QtWidgets.QStackedLayout):
    def serialize_fields(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        for item in state["items"]:
            self.add(item)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout):
        self.add(other)
        return self

    def set_current_widget(self, widget: QtWidgets.QWidget):
        self.setCurrentWidget(widget)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    layout = StackedLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.RadioButton("Test 2")
    layout += widget2
    layout += widget3
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
