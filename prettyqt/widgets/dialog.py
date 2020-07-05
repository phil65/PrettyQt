# -*- coding: utf-8 -*-
"""
"""

from typing import Union

from qtpy import QtCore, QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import icons

QtWidgets.QDialog.__bases__ = (widgets.Widget,)


class BaseDialog(QtWidgets.QDialog):

    def __getitem__(self, index):
        return self.findChild(QtWidgets.QWidget, index)

    def __getstate__(self):
        icon = gui.Icon(self.windowIcon())
        return dict(layout=self.layout(),
                    title=self.windowTitle(),
                    is_maximized=self.isMaximized(),
                    has_sizegrip=self.isSizeGripEnabled(),
                    icon=icon if not icon.isNull() else None,
                    size=(self.size().width(), self.size().height()))

    def __setstate__(self, state):
        self.__init__()
        self.set_title(state["title"])
        self.set_icon(state["icon"])
        if state["layout"]:
            self.set_layout(state["layout"])
        self.resize(state["size"])
        self.setSizeGripEnabled(state["has_sizegrip"])
        if state["is_maximized"]:
            self.showMaximized()
        self.resize(*state["size"])
        self.box = self.layout()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_F11:
            self.showNormal() if self.isMaximized() else self.showMaximized()
        else:
            super().keyPressEvent(e)

    def delete_on_close(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def add_widget(self, widget):
        self.box += widget
        return widget

    def set_icon(self, icon: icons.IconType):
        """set the icon for the menu

        Args:
            icon: icon to use
        """
        icon = icons.get_icon(icon, color="lightgray")
        self.setWindowIcon(icon)

    def add_buttonbox(self):
        button_box = widgets.DialogButtonBox.create(ok=self.accept,
                                                    cancel=self.reject)
        self.box += button_box
        return button_box

    def show_blocking(self) -> bool:
        self.show()
        return bool(self.exec_())

    def is_accepted(self):
        return self.result() == QtWidgets.QDialog.Accepted


class Dialog(BaseDialog):

    DEFAULT_SIZE = None

    def __init__(self,
                 title: str = "",
                 icon=None,
                 parent=None,
                 delete_on_close: bool = True,
                 layout: Union[None, str, QtWidgets.QLayout] = None):
        super().__init__(parent=parent)
        if self.DEFAULT_SIZE:
            self.resize(*self.DEFAULT_SIZE)
        self.set_title(title)
        self.set_icon(icon)
        if delete_on_close:
            self.delete_on_close()
        if layout is not None:
            self.set_layout(layout)


if __name__ == "__main__":
    app = widgets.app()
    w = Dialog()
    import pickle
    with open("data.pkl", "wb") as jar:
        pickle.dump(w, jar)
    with open("data.pkl", "rb") as jar:
        w = pickle.load(jar)
    w.show_blocking()
