from typing import Dict, Optional

from qtpy import QtWidgets

from prettyqt import core, gui, widgets


class BoolDictToolButton(widgets.ToolButton):
    value_changed = core.Signal(dict)

    def __init__(
        self,
        title: str,
        icon: gui.icon.IconType = None,
        dct: Dict[str, str] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent=parent)
        self.set_text(title)
        self.set_icon(icon)
        menu = widgets.Menu()
        self.set_menu(menu)
        self.set_popup_mode("instant")
        if dct:
            self.set_dict(dct)

    def __getitem__(self, key: str) -> bool:
        menu = self.menu()
        return menu[key].isChecked()

    def __setitem__(self, key: str, value: bool):
        menu = self.menu()
        menu[key].setChecked(value)
        self.value_changed.emit(self.as_dict())

    def set_dict(self, dct: Dict[str, str]):
        menu = self.menu()
        menu.clear()
        for k, v in dct.items():
            action = widgets.Action()
            action.set_text(v)
            action.setCheckable(True)
            action.set_id(k)
            action.triggered.connect(lambda: self.value_changed.emit(self.as_dict()))
            menu.add(action)
        self.value_changed.emit(self.as_dict())

    def as_dict(self) -> Dict[str, bool]:
        return {act.get_id(): act.isChecked() for act in self.menu()}


if __name__ == "__main__":
    app = widgets.app()
    dct = dict(a="test", b="test2")
    w = BoolDictToolButton("Title", None, dct)
    w.show()
    app.main_loop()
