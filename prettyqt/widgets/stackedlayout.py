# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStackedLayout.__bases__ = (widgets.Layout,)


class StackedLayout(QtWidgets.QStackedLayout):
    def __getstate__(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.add(item)

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            self.add(other)
            return self

    def set_current_widget(self, widget):
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
    app.exec_()
