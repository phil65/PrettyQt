# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
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

    def __iter__(self):
        return iter(self.get_children())

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            self.add(other)
            return self

    def get_children(self):
        return [self[i] for i in range(self.count())]


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
