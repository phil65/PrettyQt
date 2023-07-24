from __future__ import annotations

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.utils import colors, datatypes, get_repr


class ColorChooserButton(widgets.Widget):
    value_changed = core.Signal(gui.Color)

    def __init__(
        self,
        *args,
        color: datatypes.ColorType | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        layout = self.set_layout("horizontal", margin=0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_regex_validator(r"^#(?:[0-9a-fA-F]{6})$")
        layout.add(self.lineedit)
        action = gui.Action(icon="mdi.format-color-fill", triggered=self.choose_color)
        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout.add(self.button)
        self._current_color: gui.Color = gui.Color("white")
        if color is not None:
            self.set_current_color(color)

    def __repr__(self):
        return get_repr(self, self._current_color)

    @core.Slot()
    def choose_color(self):
        dlg = widgets.ColorDialog()
        if self._current_color:
            dlg.setCurrentColor(self._current_color)

        if dlg.exec():
            new_color = dlg.current_color()
            self.set_current_color(new_color)
            self.value_changed.emit(new_color)

    def set_current_color(self, color: datatypes.ColorType):
        self._current_color = colors.get_color(color)
        self.lineedit.set_text(self._current_color.name().upper())
        icon = iconprovider.for_color(self._current_color)
        self.button.set_icon(icon)

    def is_valid(self) -> bool:
        return self.lineedit.is_valid()

    def get_value(self) -> gui.Color:
        return self._current_color

    def set_value(self, value: datatypes.ColorType):
        self.set_current_color(value)

    current_color = core.Property(
        gui.QColor,
        get_value,
        set_value,
        user=True,
        doc="Currently selected color",
    )


if __name__ == "__main__":
    app = widgets.app()
    btn = ColorChooserButton(color=gui.Color("green"))
    btn.show()
    app.exec()
