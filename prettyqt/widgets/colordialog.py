# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import colors


OPTIONS = dict(
    show_alpha=QtWidgets.QColorDialog.ShowAlphaChannel,
    no_buttons=QtWidgets.QColorDialog.NoButtons,
    no_native=QtWidgets.QColorDialog.DontUseNativeDialog,
)


QtWidgets.QColorDialog.__bases__ = (widgets.BaseDialog,)


class ColorDialog(QtWidgets.QColorDialog):
    def __getstate__(self):
        return dict(color=self.current_color())

    def __setstate__(self, state):
        self.__init__()
        if state["color"]:
            self.setCurrentColor(state["color"])

    @classmethod
    def get_color(
        cls, preset: colors.ColorType = None, allow_alpha: bool = False, parent=None
    ) -> gui.Color:
        preset = colors.get_color(preset)
        kwargs = dict(options=cls.ShowAlphaChannel) if allow_alpha else dict()
        return gui.Color(cls.getColor(preset, parent, **kwargs))

    def current_color(self) -> gui.Color:
        return gui.Color(self.currentColor())


if __name__ == "__main__":
    app = widgets.app()
    ColorDialog.get_color()
    app.exec_()
