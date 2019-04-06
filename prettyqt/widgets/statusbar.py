# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
from prettyqt import widgets


class StatusBar(QtWidgets.QStatusBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progress_bar = widgets.ProgressBar()

    def setup_default_bar(self):
        # This is simply to show the bar
        self.progress_bar.hide()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedSize(200, 20)
        self.progress_bar.setTextVisible(False)
        self.addPermanentWidget(self.progress_bar)

    def add_action(self, action):
        self.addAction(action)


if __name__ == "__main__":
    import sys
    app = widgets.Application(sys.argv)
    dlg = widgets.MainWindow()
    status_bar = StatusBar()
    status_bar.setup_default_bar()
    dlg.setStatusBar(status_bar)
    dlg.show()
    app.exec_()
