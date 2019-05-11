# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets

from prettyqt import widgets, gui


class ToolBox(QtWidgets.QToolBox):

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.widget(index)
        else:
            return self.findChild(widgets.Widget, index)

    def __getstate__(self):
        children = list()
        for i, widget in enumerate(self.get_children()):
            dct = dict(widget=widget,
                       icon=gui.Icon(self.itemIcon(i)),
                       text=self.itemText(i),
                       enabled=self.isItemEnabled(i),
                       tooltip=self.itemToolTip(i))
            children.append(dct)
        return dict(items=children,
                    current_index=self.currentIndex())

    def __setstate__(self, state):
        self.__init__()
        for i, item in enumerate(state["items"]):
            self.addItem(item["widget"], item["icon"], item["text"])
            self.setItemEnabled(i, item["enabled"])
            self.setItemToolTip(i, item["tooltip"])
        self.setCurrentIndex(state["current_index"])

    def __iter__(self):
        return iter(self.get_children())

    def get_children(self):
        return [self[i] for i in range(self.count())]

    def add_widget(self, widget, title=None, icon=None):
        if title is None:
            title = widget.objectName()
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.addItem(widget, icon, title)
        else:
            self.addItem(widget, title)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    w = widgets.Widget()
    w2 = widgets.Widget()
    w2.setObjectName("objectName")
    tb = ToolBox()
    tb.add_widget(w, "title")
    tb.add_widget(w2)
    print(len(tb))
    tb.show()
    app.exec_()
