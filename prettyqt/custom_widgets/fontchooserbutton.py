# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys

from prettyqt import core, gui, widgets


class FontChooserButton(widgets.Widget):

    value_changed = core.Signal(gui.Font)

    def __init__(self, font=None, parent=None):
        super().__init__(parent)
        self.current_font = font
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit(self)
        self.lineedit.set_read_only()
        layout += self.lineedit
        action = widgets.Action()
        action.triggered.connect(self.choose_font)
        self.button = widgets.ToolButton(self)
        self.button.setDefaultAction(action)
        layout += self.button

    def __repr__(self):
        return f"FontChooserButton({self.current_font})"

    def __getstate__(self):
        return dict(font=self.current_font,
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__()
        if state["font"]:
            self.set_font(state["font"])
        self.setEnabled(state["enabled"])

    @core.Slot()
    def choose_font(self):
        dlg = widgets.FontDialog()
        if self.current_font:
            dlg.setCurrentFont(self.current_font)

        if dlg.exec_():
            self.set_font(dlg.current_font())
            self.value_changed.emit(dlg.current_font())

    def set_font(self, font):
        if isinstance(font, str):
            self.current_font = gui.Font(font)
        else:
            self.current_font = font
        self.lineedit.setText(self.current_font.family())


if __name__ == "__main__":
    app = widgets.Application(sys.argv)
    btn = FontChooserButton()
    btn.set_font("Consolas")
    btn.show()
    btn.value_changed.connect(print)
    sys.exit(app.exec_())
