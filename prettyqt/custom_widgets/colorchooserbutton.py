# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys

from prettyqt import core, widgets, gui


class ColorChooserButton(widgets.Widget):

    color_updated = core.Signal(gui.Color)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = None
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit(self)
        self.lineedit.set_regex_validator(r"^#(?:[0-9a-fA-F]{6})$")
        layout.addWidget(self.lineedit)
        action = widgets.Action()
        action.triggered.connect(self.choose_color)
        self.button = widgets.ToolButton(self)
        self.button.setDefaultAction(action)
        layout.addWidget(self.button)

    @core.Slot()
    def choose_color(self):
        dlg = widgets.ColorDialog()
        if self.color:
            dlg.setCurrentColor(self.color)

        if dlg.exec_():
            self.set_color(dlg.current_color())
            self.color_updated.emit(dlg.current_color())

    def set_color(self, color):
        self.color = gui.Color(color)
        self.lineedit.setText(self.color.name().upper())
        self.button.setStyleSheet(f"background-color: {self.color.name()};")


if __name__ == "__main__":
    app = widgets.Application(sys.argv)
    btn = ColorChooserButton()
    btn.show()
    btn.color_updated.connect(print)
    sys.exit(app.exec_())
