# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict
from qtpy import QtCore, QtWidgets

from prettyqt import widgets

ORIENTATIONS = bidict(dict(horizontal=QtCore.Qt.Horizontal,
                           vertical=QtCore.Qt.Vertical))


class Splitter(QtWidgets.QSplitter):

    def __init__(self, orientation="horizontal", parent=None):
        super().__init__(ORIENTATIONS[orientation], parent)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.widget(index)
        else:
            return self.findChild(widgets.Widget, index)

    def __getstate__(self):
        return dict(items=self.get_children(),
                    orientation=self.get_orientation(),
                    handle_width=self.handleWidth(),
                    children_collapsible=self.childrenCollapsible(),
                    opaque_resize=self.opaqueResize())

    def __setstate__(self, state):
        self.__init__(state["orientation"])
        for item in state["items"]:
            self.addWidget(item)
        self.setHandleWidth(state["handle_width"])
        self.setChildrenCollapsible(state["children_collapsible"])
        self.setOpaqueResize(state["opaque_resize"])

    def __iter__(self):
        return iter(self.get_children())

    def __len__(self):
        return self.count()

    def __add__(self, other):
        if isinstance(other, QtWidgets.QWidget):
            self.add_widget(other)
            return self
        raise TypeError(f"Invalid type: {type(other)}")

    def get_children(self):
        return [self[i] for i in range(self.count())]

    def add_widget(self, widget):
        self.addWidget(widget)

    @classmethod
    def from_widgets(cls, widgets, horizontal: bool = False, parent=None):
        orientation = "horizontal" if horizontal else "vertical"
        splitter = cls(orientation, parent=parent)
        for widget in widgets:
            splitter += widget
        return splitter

    def set_expanding(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)

    def set_orientation(self, orientation):
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self):
        return ORIENTATIONS.inv[self.orientation()]


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Splitter()
    widget.show()
    app.exec_()
