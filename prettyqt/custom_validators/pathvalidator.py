# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtGui


class PathValidator(QtGui.QValidator):

    def validate(self, text, pos=0):
        if pathlib.Path(text).exists():
            return (self.Acceptable, text, pos)
        return (self.Intermediate, text, pos)


if __name__ == "__main__":
    from prettyqt import widgets
    val = PathValidator()
    app = widgets.Application.create_default_app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec_()
