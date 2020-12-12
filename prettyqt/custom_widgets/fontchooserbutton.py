from typing import Optional

from qtpy import QtWidgets

from prettyqt import core, gui, widgets


class FontChooserButton(widgets.Widget):

    value_changed = core.Signal(gui.Font)

    def __init__(self, font=None, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self._current_font = font
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_read_only()
        layout += self.lineedit
        action = widgets.Action()
        action.triggered.connect(self.choose_font)
        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout += self.button

    def __repr__(self):
        return f"{type(self).__name__}({self._current_font})"

    def serialize_fields(self):
        return dict(font=self._current_font)

    def __setstate__(self, state):
        if state["font"]:
            self.set_font(state["font"])
        self.set_enabled(state.get("enabled", True))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    @core.Slot()
    def choose_font(self):
        dlg = widgets.FontDialog()
        if self._current_font:
            dlg.setCurrentFont(self._current_font)

        if dlg.exec_():
            self.set_font(dlg.current_font())
            self.value_changed.emit(dlg.current_font())

    def set_font(self, font):
        if isinstance(font, str):
            self._current_font = gui.Font(font)
        else:
            self._current_font = font
        self.lineedit.setText(self._current_font.family())

    def set_value(self, value):
        self.set_font(value)

    def get_value(self):
        return self._current_font


if __name__ == "__main__":
    app = widgets.app()
    btn = FontChooserButton()
    btn.set_font("Consolas")
    btn.show()
    btn.value_changed.connect(print)
    app.main_loop()
