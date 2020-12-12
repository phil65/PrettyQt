from typing import Optional

from qtpy import QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import colors


OPTIONS = dict(
    show_alpha=QtWidgets.QColorDialog.ShowAlphaChannel,
    no_buttons=QtWidgets.QColorDialog.NoButtons,
    no_native=QtWidgets.QColorDialog.DontUseNativeDialog,
)


QtWidgets.QColorDialog.__bases__ = (widgets.BaseDialog,)


class ColorDialog(QtWidgets.QColorDialog):
    def serialize_fields(self):
        return dict(color=self.current_color())

    def __setstate__(self, state):
        if state["color"]:
            self.setCurrentColor(state["color"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    @classmethod
    def get_color(
        cls,
        preset: colors.ColorType = None,
        allow_alpha: bool = False,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> gui.Color:
        preset = colors.get_color(preset)
        kwargs = dict(options=cls.ShowAlphaChannel) if allow_alpha else dict()
        return gui.Color(cls.getColor(preset, parent, **kwargs))

    def current_color(self) -> gui.Color:
        return gui.Color(self.currentColor())


if __name__ == "__main__":
    app = widgets.app()
    ColorDialog.get_color()
    app.main_loop()
