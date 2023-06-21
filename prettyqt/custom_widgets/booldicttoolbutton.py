from __future__ import annotations

from prettyqt import core, gui, widgets


class BoolDictToolButton(widgets.ToolButton):
    value_changed = core.Signal(dict)

    def __init__(
        self,
        *args,
        dct: dict[str, str] | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.button_menu = widgets.Menu(triggered=self._on_menu_click)
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
            action = gui.Action(text=v, checkable=True, object_name=k)
            self.button_menu.add(action)
        self.value_changed.emit(self.as_dict())

    def as_dict(self) -> dict[str, bool]:
        return {act.objectName(): act.isChecked() for act in self.button_menu}


if __name__ == "__main__":
    app = widgets.app()
    dct = dict(a="test", b="test2")
    w = BoolDictToolButton(text="Title", dct=dct)
    w.show()
    app.exec()
