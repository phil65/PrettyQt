from __future__ import annotations

from typing import Literal

from prettyqt import gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import bidict, colors, datatypes


OptionStr = Literal["show_alpha", "no_buttons", "no_native"]

OPTIONS: bidict[OptionStr, QtWidgets.QColorDialog.ColorDialogOption] = bidict(
    show_alpha=QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel,
    no_buttons=QtWidgets.QColorDialog.ColorDialogOption.NoButtons,
    no_native=QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog,
)


class ColorDialog(widgets.DialogMixin, QtWidgets.QColorDialog):
    @classmethod
    def get_color(
        cls,
        preset: datatypes.ColorType = None,
        allow_alpha: bool = False,
        parent: QtWidgets.QWidget | None = None,
    ) -> gui.Color:
        preset = colors.get_color(preset)
        kwargs = (
            dict(options=cls.ColorDialogOption.ShowAlphaChannel) if allow_alpha else {}
        )
        color = cls.getColor(preset, parent, **kwargs)  # type: ignore
        return gui.Color(color)

    def current_color(self) -> gui.Color:
        return gui.Color(self.currentColor())

    def get_qcolorshower(self) -> QtWidgets.QWidget:
        return [
            a
            for a in self.children()
            if hasattr(a, "metaObject")
            and a.metaObject().className() == "QtPrivate::QColorShower"
        ][0]

    def get_qcolorshowlabel(self) -> QtWidgets.QFrame:
        qcs = self.get_qcolorshower()
        return [
            b
            for b in qcs.children()
            if hasattr(b, "metaObject")
            and b.metaObject().className() == "QtPrivate::QColorShowLabel"
        ][0]

    def replace_qcolorshowlabel(self, widget: QtWidgets.QWidget):
        # Find the dialog widget used to display the current
        # color, so we can replace it with our implementation
        qcs = self.get_qcolorshower()
        qcsl = self.get_qcolorshowlabel()
        qcs.layout().replaceWidget(qcsl, widget)
        # Make sure it doesn't receive signals while hidden
        qcsl.blockSignals(True)
        qcsl.hide()
        widget.show()

    def use_alpha_channel(self, value: bool = True):
        self.setOption(self.ColorDialogOption.ShowAlphaChannel, value)

    def hide_buttons(self, value: bool = True):
        self.setOption(self.ColorDialogOption.NoButtons, value)

    def use_native_dialog(self, value: bool = True):
        self.setOption(self.ColorDialogOption.DontUseNativeDialog, not value)

    @classmethod
    def get_custom_colors(cls) -> list[gui.Color]:
        return [gui.Color(cls.customColor(i)) for i in range(cls.customCount())]

    @classmethod
    def set_custom_colors(cls, colors_: list[datatypes.ColorType]):
        num = min(len(colors_), cls.customCount())
        for i in range(num):
            color = colors.get_color(colors_[i])
            cls.setCustomColor(i, color)


class CPAlphaShowLabel(widgets.Label):
    """Label which displays the currently-active color using checkerboard alpha.

    A replacement for QColorDialog's QColorShowLabel.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Length in pixels of a side of the checkerboard squares
        # (Pattern is made up of 2x2 squares, total size 2n x 2n)
        self.checkerboard_size = 8
        # Start out transparent by default
        self.color = self.parent().currentColor()
        self.parent().currentColorChanged.connect(self.update_color)
        self.pattern = gui.Pixmap.create_checkerboard_pattern(
            self.checkerboard_size, "#aaa", "#ccc"
        )

    def update_color(self, color: QtGui.QColor):
        self.color = color
        self.repaint()

    def paintEvent(self, event):
        """Show the current color using checkerboard alpha."""
        event.accept()
        with gui.Painter(self) as p:
            p.set_pen(None)
            if self.color.alphaF() < 1.0:
                p.drawTiledPixmap(event.rect(), self.pattern, QtCore.QPoint(4, 4))
            p.fillRect(event.rect(), self.color)


if __name__ == "__main__":
    app = widgets.app()
    dlg = ColorDialog()
    dlg.setOptions(ColorDialog.ColorDialogOption.ShowAlphaChannel)  # type: ignore
    label = CPAlphaShowLabel(dlg)
    dlg.replace_qcolorshowlabel(label)
    cs = dlg.get_qcolorshower()
    dlg.show()
    with app.debug_mode():
        app.exec()
