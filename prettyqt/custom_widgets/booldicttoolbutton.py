from typing import Dict, Optional

from qtpy import QtWidgets

from prettyqt import core, iconprovider, widgets


class BoolDictToolButton(widgets.ToolButton):
    value_changed = core.Signal(dict)

    def __init__(
        self,
        title: str,
        icon: iconprovider.IconType = None,
        dct: Dict[str, str] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent=parent)
        self.set_text(title)
        self.set_icon(icon)
        self.button_menu = widgets.Menu()
        self.setMenu(self.button_menu)
        self.set_popup_mode("instant")
        if dct:
            self.set_dict(dct)

    def __getitem__(self, key: str) -> bool:  # type: ignore
        return self.button_menu[key].isChecked()

    def __setitem__(self, key: str, value: bool):
        self.button_menu[key].setChecked(value)
        self.value_changed.emit(self.as_dict())

    def set_dict(self, dct: Dict[str, str]):
        self.button_menu.clear()
        for k, v in dct.items():
            action = widgets.Action()
            action.set_text(v)
            action.setCheckable(True)
            action.set_id(k)
            action.triggered.connect(lambda: self.value_changed.emit(self.as_dict()))
            self.button_menu.add(action)
        self.value_changed.emit(self.as_dict())

    def as_dict(self) -> Dict[str, bool]:
        return {act.get_id(): act.isChecked() for act in self.button_menu}


if __name__ == "__main__":
    app = widgets.app()
    dct = dict(a="test", b="test2")
    w = BoolDictToolButton("Title", None, dct)
    w.show()
    app.main_loop()
