# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QProgressDialog.__bases__ = (widgets.BaseDialog,)


class ProgressDialog(QtWidgets.QProgressDialog):
    """Progress dialog

    wrapper for QtWidgets.QProgressDialog
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        progress_bar = widgets.ProgressBar()
        progress_bar.setRange(0, 0)
        progress_bar.setTextVisible(False)
        self.setBar(progress_bar)

        self.set_icon("mdi.timer-sand-empty")
        self.set_modality("application")
        self.set_flags(
            minimize=False, maximize=False, close=False, stay_on_top=True, window=True
        )
        self.setCancelButton(None)
        self.cancel()

    def show_message(self, message: str):
        self.setLabelText(message)
        self.show()


if __name__ == "__main__":
    app = widgets.app()
    widget = ProgressDialog()
    widget.show_message("test")
    widget.exec_()
