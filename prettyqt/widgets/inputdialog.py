from typing import List, Optional

from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QInputDialog.__bases__ = (widgets.BaseDialog,)


class InputDialog(QtWidgets.QInputDialog):
    @classmethod
    def get_int(
        cls,
        title: Optional[str] = None,
        label: Optional[str] = None,
        icon: gui.icon.IconType = None,
    ) -> Optional[int]:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getInt(par, title, label)
        return v[0] if v[1] else None

    @classmethod
    def get_float(
        cls,
        title: Optional[str] = None,
        label: Optional[str] = None,
        icon: gui.icon.IconType = None,
    ) -> Optional[float]:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getDouble(par, title, label)
        return v[0] if v[1] else None

    @classmethod
    def get_text(
        cls,
        title: Optional[str] = None,
        label: Optional[str] = None,
        icon: gui.icon.IconType = None,
        default_value: str = "",
    ) -> Optional[str]:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getText(par, title, label, text=default_value)
        return v[0] if v[1] else None

    @classmethod
    def get_item(
        cls,
        items: List[str],
        title: Optional[str] = None,
        label: Optional[str] = None,
        icon: gui.icon.IconType = None,
        editable: bool = False,
    ) -> Optional[str]:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getItem(par, title, label, items, editable=editable)
        return v[0] if v[1] else None


if __name__ == "__main__":
    app = widgets.app()
    result = InputDialog.get_text("a", "b", icon="mdi.timer")
    print(result)
    app.main_loop()
