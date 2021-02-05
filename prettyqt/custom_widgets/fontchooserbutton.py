from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtGui, QtWidgets


class FontChooserButton(widgets.Widget):

    value_changed = core.Signal(gui.Font)

    def __init__(
        self,
        font: QtGui.QFont | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self._current_font = font
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_read_only()
        layout.add(self.lineedit)
        action = widgets.Action()
        action.triggered.connect(self.choose_font)
        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout.add(self.button)

    def __repr__(self):
        return f"{type(self).__name__}({self._current_font})"

    def serialize_fields(self):
        return dict(current_font=self._current_font)

    def __setstate__(self, state):
        super().__setstate__(state)
        if state["current_font"]:
            self.set_value(state["current_font"])
        self.set_enabled(state.get("enabled", True))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    @core.Slot()
    def choose_font(self):
        dlg = widgets.FontDialog()
        if self._current_font:
            dlg.setCurrentFont(self._current_font)

        if dlg.main_loop():
            self.set_current_font(dlg.current_font())
            self.value_changed.emit(dlg.current_font())

    def set_current_font(self, font: str | QtGui.QFont):
        if isinstance(font, str):
            self._current_font = gui.Font(font)
        else:
            self._current_font = font
        self.lineedit.setText(self._current_font.family())

    def set_value(self, value: str | QtGui.QFont):
        self.set_current_font(value)

    def get_value(self):
        return self._current_font


if __name__ == "__main__":
    app = widgets.app()
    btn = FontChooserButton()
    btn.set_current_font("Consolas")
    btn.show()
    btn.value_changed.connect(print)
    app.main_loop()
