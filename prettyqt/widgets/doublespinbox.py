# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = DoubleSpinBox()
    widget.show()
    app.exec_()
