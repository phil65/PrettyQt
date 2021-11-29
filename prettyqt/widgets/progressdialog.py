from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QProgressDialog.__bases__ = (widgets.Dialog,)


class ProgressDialog(QtWidgets.QProgressDialog):
    """Progress dialog.

    Wrapper for QtWidgets.QProgressDialog
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None):
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
        self.setCancelButton(None)  # type: ignore
        self.cancel()

    def show_message(self, message: str):
        self.setLabelText(message)
        self.show()


if __name__ == "__main__":
    app = widgets.app()
    widget = ProgressDialog()
    widget.show_message("test")
    widget.main_loop()
