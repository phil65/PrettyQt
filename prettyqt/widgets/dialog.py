# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Optional

import qtawesome as qta
from qtpy import QtCore, QtWidgets

from prettyqt import widgets, gui

MODALITIES = dict(window=QtCore.Qt.WindowModal,
                  application=QtCore.Qt.ApplicationModal)


class Dialog(QtWidgets.QDialog):

    DEFAULT_SIZE = None

    def __init__(self,
                 title: str = "",
                 icon=None,
                 parent=None,
                 delete_on_close: bool = True,
                 layout: Optional[str] = None):
        super().__init__(parent=parent)
        if self.DEFAULT_SIZE:
            self.resize(*self.DEFAULT_SIZE)
        self.setWindowTitle(title)
        self.set_icon(icon)
        if delete_on_close:
            self.delete_on_close()
        self.box = None
        if layout in ["horizontal", "vertical"]:
            self.box = widgets.BoxLayout(layout)
            self.setLayout(self.box)

    def __getitem__(self, index):
        return self.findChild(QtWidgets.QWidget, index)

    def __getstate__(self):
        return dict(layout=self.layout(),
                    title=self.windowTitle(),
                    is_maximized=self.isMaximized(),
                    has_sizegrip=self.isSizeGripEnabled(),
                    icon=gui.Icon(self.windowIcon()),
                    size=(self.size().width(), self.size().height()))

    def __setstate__(self, state):
        super().__init__()
        self.setWindowTitle(state["title"])
        self.set_icon(state["icon"])
        if state["layout"]:
            self.setLayout(state["layout"])
        self.resize(state["size"])
        self.setSizeGripEnabled(state["has_sizegrip"])
        if state["is_maximized"]:
            self.showMaximized()
        self.resize(*state["size"])

    def resize(self, *size):
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def set_modality(self, modality: str = "window"):
        if modality not in MODALITIES:
            raise ValueError("Invalid value for modality.")
        self.setWindowModality(MODALITIES[modality])

    def delete_on_close(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def add_widget(self, widget):
        self.box += widget
        return widget

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)

    def add_buttonbox(self):
        button_box = widgets.DialogButtonBox()
        button_box.add_buttons(["cancel", "ok"])
        button_box.accepted.connect(self.accepted)
        button_box.rejected.connect(self.reject)
        self.box += button_box

    def accepted(self):
        self.close()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        else:
            super().keyPressEvent(e)

    def open(self):
        self.show()
        self.exec_()


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = Dialog()
    import pickle
    with open("data.pkl", 'wb') as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", 'rb') as jar:
        widget = pickle.load(jar)
    widget.show()
    app.exec_()
