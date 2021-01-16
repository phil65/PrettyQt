from __future__ import annotations

from typing import Literal, Optional

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import colors, types


OPTIONS = dict(
    show_alpha=QtWidgets.QColorDialog.ShowAlphaChannel,
    no_buttons=QtWidgets.QColorDialog.NoButtons,
    no_native=QtWidgets.QColorDialog.DontUseNativeDialog,
)

OptionStr = Literal["show_alpha", "no_buttons", "no_native"]

QtWidgets.QColorDialog.__bases__ = (widgets.BaseDialog,)


class ColorDialog(QtWidgets.QColorDialog):
    def serialize_fields(self):
        return dict(color=self.current_color())

    def __setstate__(self, state):
        super().__setstate__(state)
        if state["color"]:
            self.setCurrentColor(state["color"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    @classmethod
    def get_color(
        cls,
        preset: types.ColorType = None,
        allow_alpha: bool = False,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> gui.Color:
        preset = colors.get_color(preset)
        kwargs = dict(options=cls.ShowAlphaChannel) if allow_alpha else {}
        color = cls.getColor(preset, parent, **kwargs)
        return gui.Color(color)

    def current_color(self) -> gui.Color:
        return gui.Color(self.currentColor())

    def get_qcolorshower(self) -> QtWidgets.QWidget:
        return [
            a
            for a in self.children()
            if hasattr(a, "metaObject") and a.metaObject().className() == "QColorShower"
        ][0]

    def get_qcolorshowlabel(self) -> QtWidgets.QFrame:
        qcs = self.get_qcolorshower()
        return [
            b
            for b in qcs.children()
            if hasattr(b, "metaObject")
            and b.metaObject().className() == "QColorShowLabel"
        ][0]


if __name__ == "__main__":
    app = widgets.app()
    dlg = ColorDialog()
    cs = dlg.get_qcolorshower()
    print(type(cs))
    app.main_loop()
