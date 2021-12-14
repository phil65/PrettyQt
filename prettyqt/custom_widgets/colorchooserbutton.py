from __future__ import annotations

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import colors, types


class ColorChooserButton(widgets.Widget):

    value_changed = core.Signal(gui.Color)

    def __init__(
        self, color: types.ColorType = None, parent: QtWidgets.QWidget | None = None
    ):
        super().__init__(parent)
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_regex_validator(r"^#(?:[0-9a-fA-F]{6})$")
        layout.add(self.lineedit)
        action = widgets.Action(icon="mdi.format-color-fill")
        action.triggered.connect(self.choose_color)
        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout.add(self.button)
        self._current_color: gui.Color = gui.Color("white")
        if color is not None:
            self.set_current_color(color)

    def __repr__(self):
        return f"{type(self).__name__}({self._current_color})"

    def serialize_fields(self):
        return dict(current_color=self._current_color, enabled=self.isEnabled())

    def __setstate__(self, state):
        if state["current_color"]:
            self.set_current_color(state["current_color"])
        self.setEnabled(state.get("enabled", True))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    @core.Slot()
    def choose_color(self):
        dlg = widgets.ColorDialog()
        if self._current_color:
            dlg.setCurrentColor(self._current_color)

        if dlg.main_loop():
            new_color = dlg.current_color()
            self.set_current_color(new_color)
            self.value_changed.emit(new_color)

    def set_current_color(self, color: types.ColorType):
        self._current_color = colors.get_color(color)
        self.lineedit.set_text(self._current_color.name().upper())
        icon = iconprovider.for_color(self._current_color)
        self.button.set_icon(icon)

    def is_valid(self) -> bool:
        return self.lineedit.is_valid()

    def get_value(self) -> gui.Color:
        return self._current_color

    def set_value(self, value: types.ColorType):
        self.set_current_color(value)


if __name__ == "__main__":
    app = widgets.app()
    btn = ColorChooserButton(gui.Color("green"))
    btn.show()
    btn.value_changed.connect(print)
    app.main_loop()
