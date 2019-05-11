# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import widgets


class Splitter(QtWidgets.QSplitter):

    def __init__(self, orientation="horizontal", parent=None):
        o = QtCore.Qt.Vertical if orientation == "vertical" else QtCore.Qt.Horizontal
        super().__init__(o, parent)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.widget(index)
        else:
            return self.findChild(widgets.Widget, index)

    def __getstate__(self):
        return dict(items=self.get_children(),
                    orientation=self.orientation(),
                    handle_width=self.handleWidth(),
                    children_collapsible=self.childrenCollapsible(),
                    opaque_resize=self.opaqueResize())

    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.addWidget(item)
        self.setOrientation(state["orientation"])
        self.setHandleWidth(state["handle_width"])
        self.setChildrenCollapsible(state["children_collapsible"])
        self.setOpaqueResize(state["opaque_resize"])

    def __iter__(self):
        return iter(self.get_children())

    def __len__(self):
        return self.count()

    def get_children(self):
        return [self[i] for i in range(self.count())]

    def add_widget(self, widget):
        self.addWidget(widget)

    @classmethod
    def from_widgets(cls, widgets, horizontal: bool = False, parent=None):
        orientation = QtCore.Qt.Horizontal if horizontal else QtCore.Qt.Vertical
        splitter = cls(orientation, parent=parent)
        for widget in widgets:
            splitter.addWidget(widget)
        return splitter

    def set_expanding(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Splitter()
    widget.show()
    app.exec_()
