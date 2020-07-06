# -*- coding: utf-8 -*-
"""
"""

from prettyqt import core, gui, widgets
from prettyqt.utils import colors


class ColorChooserButton(widgets.Widget):

    value_changed = core.Signal(gui.Color)

    def __init__(self, color=None, parent=None):
        super().__init__(parent)
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_regex_validator(r"^#(?:[0-9a-fA-F]{6})$")
        layout += self.lineedit
        action = widgets.Action(icon="mdi.format-color-fill")
        action.triggered.connect(self.choose_color)
        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout += self.button
        if color is not None:
            self.set_color(color)

    def __repr__(self):
        return f"ColorChooserButton({self.current_color})"

    def __getstate__(self):
        return dict(color=self.current_color, enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__()
        if state["color"]:
            self.set_color(state["color"])
        self.setEnabled(state.get("enabled", True))

    @core.Slot()
    def choose_color(self):
        dlg = widgets.ColorDialog()
        if self.current_color:
            dlg.setCurrentColor(self.current_color)

        if dlg.exec_():
            self.set_color(dlg.current_color())
            self.value_changed.emit(dlg.current_color())

    def set_color(self, color: colors.ColorType):
        self.current_color = colors.get_color(color)
        self.lineedit.set_text(self.current_color.name().upper())
        icon = gui.Icon.for_color(self.current_color)
        self.button.set_icon(icon)

    def is_valid(self) -> bool:
        return self.lineedit.is_valid()

    def get_value(self):
        return self.current_color

    def set_value(self, value):
        self.set_color(value)


if __name__ == "__main__":
    app = widgets.app()
    btn = ColorChooserButton(gui.Color("green"))
    btn.show()
    btn.value_changed.connect(print)
    app.exec_()
