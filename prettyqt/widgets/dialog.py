# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Optional, Union

from bidict import bidict
import qtawesome as qta
from qtpy import QtCore, QtWidgets, QtGui

from prettyqt import widgets, gui

MODALITIES = bidict(dict(window=QtCore.Qt.WindowModal,
                         application=QtCore.Qt.ApplicationModal,
                         none=QtCore.Qt.NonModal))


class BaseDialog(QtWidgets.QDialog):

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
        self.__init__()
        self.setWindowTitle(state["title"])
        self.set_icon(state["icon"])
        if state["layout"]:
            self.setLayout(state["layout"])
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
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        else:
            super().keyPressEvent(e)

    def set_modality(self, modality: str = "window"):
        """set modality for the dialog

        Valid values for modality: "modeless", "window", "application"

        Args:
            modality: modality for the main window (default: {"window"})

        Raises:
            ValueError: modality type does not exist
        """
        if modality not in MODALITIES:
            raise ValueError("Invalid value for modality.")
        self.setWindowModality(MODALITIES[modality])

    def get_modality(self) -> str:
        """get the current modality modes as a string

        Possible values: "modeless", "window", "application"

        Returns:
            modality mode
            str
        """
        return MODALITIES.inv[self.windowModality()]

    def delete_on_close(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def add_widget(self, widget):
        self.box += widget
        return widget

    def set_icon(self, icon: Union[QtGui.QIcon, str, None]):
        """set the icon for the menu

        Args:
            icon: icon to use
        """
        if icon is None:
            icon = gui.Icon()
        elif isinstance(icon, str):
            icon = qta.icon(icon, color="lightgray")
        self.setWindowIcon(icon)

    def add_buttonbox(self):
        button_box = widgets.DialogButtonBox.create(ok=self.accepted,
                                                    cancel=self.reject)
        self.box += button_box
        return button_box

    def accepted(self):
        self.close()

    def show_blocking(self):
        self.show()
        self.exec_()

    def set_flags(self,
                  minimize: bool = None,
                  maximize: bool = None,
                  close: bool = None,
                  stay_on_top: bool = None,
                  window: bool = None):
        if minimize is not None:
            self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, minimize)
        if maximize is not None:
            self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, maximize)
        if close is not None:
            self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, close)
        if stay_on_top is not None:
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, stay_on_top)
        if window is not None:
            self.setWindowFlag(QtCore.Qt.Window, window)


BaseDialog.__bases__[0].__bases__ = (widgets.Widget,)


class Dialog(BaseDialog):

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


if __name__ == "__main__":
    app = widgets.app()
    widget = Dialog()
    import pickle
    with open("data.pkl", "wb") as jar:
        pickle.dump(widget, jar)
    with open("data.pkl", "rb") as jar:
        widget = pickle.load(jar)
    widget.show_blocking()
