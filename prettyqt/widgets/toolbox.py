# -*- coding: utf-8 -*-
"""
"""

from typing import Optional

from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QToolBox.__bases__ = (widgets.Frame,)


class ToolBox(QtWidgets.QToolBox):
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.widget(index)
        else:
            return self.findChild(QtWidgets.QWidget, index)

    def __getstate__(self):
        children = list()
        for i, widget in enumerate(self.get_children()):
            dct = dict(
                widget=widget,
                icon=gui.Icon(self.itemIcon(i)),
                text=self.itemText(i),
                enabled=self.isItemEnabled(i),
                tooltip=self.itemToolTip(i),
            )
            children.append(dct)
        return dict(items=children, current_index=self.currentIndex())

    def __setstate__(self, state):
        self.__init__()
        for i, item in enumerate(state["items"]):
            self.addItem(item["widget"], item["icon"], item["text"])
            self.setItemEnabled(i, item["enabled"])
            self.setItemToolTip(i, item["tooltip"])
        self.setCurrentIndex(state["current_index"])

    def __iter__(self):
        return iter(self.get_children())

    def get_children(self) -> list:
        return [self[i] for i in range(self.count())]

    def add_widget(
        self, widget, title: Optional[str] = None, icon: gui.icon.IconType = None
    ):
        if title is None:
            title = widget.id
        if icon:
            icon = gui.icon.get_icon(icon)
            self.addItem(widget, icon, title)
        else:
            self.addItem(widget, title)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    w2 = widgets.Widget()
    tb = ToolBox()
    tb.add_widget(w, "title")
    tb.add_widget(w2)
    print(len(tb))
    tb.show()
    app.exec_()
