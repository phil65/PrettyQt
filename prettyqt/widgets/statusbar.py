# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStatusBar.__bases__ = (widgets.Widget,)


class StatusBar(QtWidgets.QStatusBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progress_bar = widgets.ProgressBar()

    def __add__(self, other):
        if isinstance(other, QtWidgets.QAction):
            self.add_action(other)
            return self
        if isinstance(other, QtWidgets.QWidget):
            self.addWidget(other)
            return self

    def setup_default_bar(self):
        # This is simply to show the bar
        self.progress_bar.hide()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedSize(200, 20)
        self.progress_bar.setTextVisible(False)
        self.addPermanentWidget(self.progress_bar)

    def add_action(self, action):
        self.addAction(action)

    def set_color(self, color):
        self.setStyleSheet(f"background-color: {color};")

    def add_widget(self, widget, permanent=False):
        if permanent:
            self.addPermanentWidget(widget)
        else:
            self.addWidget(widget)

    def show_message(self, message: str, timeout=0):
        self.showMessage(message, timeout)


if __name__ == "__main__":
    app = widgets.app()
    dlg = widgets.MainWindow()
    status_bar = StatusBar()
    status_bar.set_color("black")
    label = widgets.Label("test")
    status_bar.addWidget(label)
    status_bar.setup_default_bar()
    dlg.setStatusBar(status_bar)
    dlg.show()
    app.exec_()
