from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.utils import get_repr


class FontChooserButton(widgets.Widget):
    value_changed = core.Signal(gui.Font)

    def __init__(
        self,
        font: gui.QFont | str | None = None,
        object_name: str = "font_chooser_button",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        self._current_font = None
        layout = self.set_layout("horizontal", margin=0)
        self.lineedit = widgets.LineEdit(read_only=True)
        self.set_current_font(font)
        layout.add(self.lineedit)
        action = gui.Action(icon="mdi.format-font", triggered=self.choose_font)
        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout.add(self.button)

    def __repr__(self):
        return get_repr(self, self.current_font)

    @core.Slot()
    def choose_font(self):
        dlg = widgets.FontDialog()
        if self._current_font:
            dlg.setCurrentFont(self._current_font)

        if dlg.exec():
            self.set_current_font(dlg.current_font())
            self.value_changed.emit(dlg.current_font())

    def set_current_font(self, font: str | gui.QFont | None):
        match font:
            case str():
                self._current_font = gui.Font(font)
            case None:
                self._current_font = gui.Font()
            case _:
                self._current_font = font
        self.lineedit.setText(self._current_font.family())

    def set_value(self, value: str | gui.QFont):
        self.set_current_font(value)

    def get_value(self) -> gui.QFont:
        return gui.QFont(self._current_font)

    current_font = core.Property(gui.QFont, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    btn = FontChooserButton()
    btn.set_current_font(gui.Font.mono())
    btn.show()
    app.exec()
