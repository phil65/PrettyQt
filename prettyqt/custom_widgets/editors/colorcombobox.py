from __future__ import annotations

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.utils import colors, datatypes, get_repr


class ColorComboBox(widgets.ComboBox):
    value_changed = core.Signal(gui.QColor)

    def __init__(
        self,
        color: datatypes.ColorType | None = None,
        object_name: str = "color_combobox",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        self._current_color: gui.QColor = gui.QColor("white")
        for i in gui.Color.colorNames():
            self.addItem(iconprovider.for_color(i), i)
        if color is not None:
            self.set_current_color(color)
        self.currentTextChanged.connect(self.set_current_color)

    def __repr__(self):
        return get_repr(self, self._current_color)

    def clear(self):
        self._current_color = gui.QColor("white")
        super().clear()
        for i in gui.Color.colorNames():
            self.addItem(iconprovider.for_color(i), i)

    def set_current_color(self, color: datatypes.ColorType):
        self._current_color = colors.get_color(color).as_qt()
        for color_name in gui.Color.colorNames():
            if gui.Color(color_name) == self._current_color:
                self.setCurrentText(color_name)
                return

    def is_valid(self) -> bool:
        return self._current_color.isValid()

    def get_value(self) -> gui.QColor:
        return self._current_color

    def set_value(self, value: datatypes.ColorType):
        self.set_current_color(value)

    current_color = core.Property(gui.QColor, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    btn = ColorComboBox(gui.Color("green"))
    btn.show()
    btn.value_changed.connect(print)
    app.exec()
