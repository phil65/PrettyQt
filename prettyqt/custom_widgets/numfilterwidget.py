from __future__ import annotations

from collections.abc import Callable
import functools
import operator

from prettyqt import core, gui, widgets


class NumFilterWidget(widgets.Widget):
    filter_changed = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout("horizontal", margin=0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_validator("double", empty_allowed=True)
        self.op_button = widgets.ToolButton()
        self.op_button.setStyleSheet("QToolButton::menu-indicator{width:0px;}")
        self.box.add(self.op_button)
        self.box.add(self.lineedit)
        self.menu = widgets.Menu(triggered=self._on_menu_click)
        for comp in ["=", "<=", "<", ">=", ">"]:
            self.menu.add_action(comp)
        self.op_button.setMenu(self.menu)
        self.op_button.set_popup_mode("instant")
        self.op_button.setText("=")
        self.lineedit.value_changed.connect(self._on_filter_change)

    def _on_filter_change(self):
        self.filter_changed.emit(self.get_filter_fn())

    def _on_menu_click(self, action: gui.QAction):
        self.op_button.setText(action.text())
        self._on_filter_change()

    def get_filter_fn(self) -> Callable:
        val = self.lineedit.get_value()
        if val == "":
            return lambda x: True
        val = float(val)
        match self.op_button.text():
            case "=":
                return functools.partial(operator.eq, val)
            case "<=":
                return functools.partial(operator.ge, val)
            case "<":
                return functools.partial(operator.gt, val)
            case ">=":
                return functools.partial(operator.le, val)
            case ">":
                return functools.partial(operator.lt, val)
            case _:
                raise ValueError


if __name__ == "__main__":
    app = widgets.app()
    widget = NumFilterWidget()
    widget.show()
    widget.filter_changed.connect(print)
    app.exec()
