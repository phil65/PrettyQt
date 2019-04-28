# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets, gui


class ColorDialog(QtWidgets.QColorDialog):

    @classmethod
    def get_color(cls, preset, parent=None):
        if isinstance(preset, str):
            preset = gui.Color(preset)
        return cls.getColor(preset, parent)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = ColorDialog()
    widget.show()
    app.exec_()
