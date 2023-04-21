from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes


class BoolDictToolButton(widgets.ToolButton):
    value_changed = core.Signal(dict)

    def __init__(
        self,
        title: str,
        icon: datatypes.IconType | None = None,
        dct: dict[str, str] | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.set_text(title)
        self.set_icon(icon)
        self.button_menu = widgets.Menu()
        self.button_menu.triggered.connect(self._on_menu_click)
        self.setMenu(self.button_menu)
        self.set_popup_mode("instant")
        if dct:
            self.set_dict(dct)

    def _on_menu_click(self):
        self.value_changed.emit(self.as_dict())

    def __getitem__(self, key: str) -> bool:  # type: ignore
        return self.button_menu[key].isChecked()

    def __setitem__(self, key: str, value: bool):
        self.button_menu[key].setChecked(value)
        self.value_changed.emit(self.as_dict())

    def set_dict(self, dct: dict[str, str]):
        self.button_menu.clear()
        for k, v in dct.items():
            action = widgets.Action()
            action.set_text(v)
            action.setCheckable(True)
            action.set_id(k)
            self.button_menu.add(action)
        self.value_changed.emit(self.as_dict())

    def as_dict(self) -> dict[str, bool]:
        return {act.get_id(): act.isChecked() for act in self.button_menu}


if __name__ == "__main__":
    app = widgets.app()
    dct = dict(a="test", b="test2")
    w = BoolDictToolButton("Title", None, dct)
    w.value_changed.connect(print)
    w.show()
    app.main_loop()
