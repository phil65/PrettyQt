# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtCore, QtWidgets
from bidict import bidict

from prettyqt import widgets

MODALITIES = bidict(dict(window=QtCore.Qt.WindowModal,
                         application=QtCore.Qt.ApplicationModal,
                         none=QtCore.Qt.NonModal))


class ProgressDialog(QtWidgets.QProgressDialog):
    """Progress dialog

    wrapper for QtWidgets.QProgressDialog
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        progress_bar = widgets.ProgressBar()
        progress_bar.setRange(0, 0)
        progress_bar.setTextVisible(False)
        self.setBar(progress_bar)

        self.set_icon("mdi.timer-sand-empty")
        self.set_modality("application")
        self.set_flags(minimize=False,
                       maximize=False,
                       close=False,
                       stay_on_top=True,
                       window=True)
        self.setCancelButton(None)
        self.cancel()

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)

    def show_message(self, message):
        self.setLabelText(message)
        self.show()

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

    def set_modality(self, modality: str = "window"):
        if modality not in MODALITIES:
            raise ValueError("Invalid value for modality.")
        self.setWindowModality(MODALITIES[modality])

    def get_modality(self):
        return MODALITIES.inv[self.windowModality()]


if __name__ == "__main__":
    app = widgets.app()
    widget = ProgressDialog()
    widget.show_message("test")
    widget.exec_()
