# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
import qtawesome as qta

from prettyqt import widgets


class ToolBox(QtWidgets.QToolBox):

    def __getitem__(self, index):
        return self.widget(index)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

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
