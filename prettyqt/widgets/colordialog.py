from __future__ import annotations

from typing import Literal

from prettyqt import gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import colors, types


OPTIONS = dict(
    show_alpha=QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel,
    no_buttons=QtWidgets.QColorDialog.ColorDialogOption.NoButtons,
    no_native=QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog,
)

OptionStr = Literal["show_alpha", "no_buttons", "no_native"]

QtWidgets.QColorDialog.__bases__ = (widgets.Dialog,)


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


class CPAlphaShowLabel(widgets.Label):
    """Label which displays the currently-active color using checkerboard alpha.

    A replacement for QColorDialog's QColorShowLabel.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        # Length in pixels of a side of the checkerboard squares
        # (Pattern is made up of 2×2 squares, total size 2n × 2n)
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
    app.main_loop()
