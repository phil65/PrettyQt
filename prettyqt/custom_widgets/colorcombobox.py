from __future__ import annotations

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import colors, datatypes, get_repr


class ColorComboBox(widgets.ComboBox):
    value_changed = core.Signal(gui.Color)

    def __init__(
        self,
        color: datatypes.ColorType | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self._current_color: gui.Color = gui.Color("white")
        for i in gui.Color.colorNames():
            self.addItem(iconprovider.for_color(i), i)
        if color is not None:
            self.set_current_color(color)
        self.currentTextChanged.connect(self.set_current_color)

    def __repr__(self):
        return get_repr(self, self._current_color)

    def set_current_color(self, color: datatypes.ColorType):
        self._current_color = colors.get_color(color)
        for color_name in gui.Color.colorNames():
            if gui.Color(color_name) == self._current_color:
                self.setCurrentText(color_name)
                return

    def is_valid(self) -> bool:
        return self._current_color.isValid()

    def get_value(self) -> gui.Color:
        return self._current_color

    def set_value(self, value: datatypes.ColorType):
        self.set_current_color(value)

    current_color = core.Property(QtGui.QColor, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    btn = ColorComboBox(gui.Color("green"))
    btn.show()
    btn.value_changed.connect(print)
    app.main_loop()