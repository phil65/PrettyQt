# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets, gui


class ColorDialog(QtWidgets.QColorDialog):

    @classmethod
    def get_color(cls, preset=None, allow_alpha=False, parent=None):
        if isinstance(preset, str):
            preset = gui.Color(preset)
        if preset is None:
            preset = gui.Color()
        kwargs = dict(options=cls.ShowAlphaChannel) if allow_alpha else dict()
        return gui.Color(cls.getColor(preset, parent, **kwargs))

    def current_color(self):
        return gui.Color(self.currentColor())


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    ColorDialog.get_color()
    app.exec_()
