from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import get_repr


class FontChooserButton(widgets.Widget):
    value_changed = core.Signal(gui.Font)

    def __init__(
        self,
        font: QtGui.QFont | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self._current_font = font or QtGui.QFont()
        layout = widgets.HBoxLayout(self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_read_only()
        layout.add(self.lineedit)
        action = gui.Action(icon="mdi.format-font")
        action.triggered.connect(self.choose_font)
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

        if dlg.main_loop():
            self.set_current_font(dlg.current_font())
            self.value_changed.emit(dlg.current_font())

    def set_current_font(self, font: str | QtGui.QFont):
        self._current_font = gui.Font(font) if isinstance(font, str) else font
        self.lineedit.setText(self._current_font.family())

    def set_value(self, value: str | QtGui.QFont):
        self.set_current_font(value)

    def get_value(self):
        return self._current_font

    current_font = core.Property(QtGui.QFont, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    btn = FontChooserButton()
    btn.set_current_font("Consolas")
    btn.show()
    btn.value_changed.connect(print)
    app.main_loop()
