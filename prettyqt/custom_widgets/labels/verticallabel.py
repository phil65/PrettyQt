from __future__ import annotations

from prettyqt import constants, core, gui, widgets


class VerticalLabel(widgets.Label):
    def __init__(
        self,
        text: str = "",
        orientation: constants.Orientation | constants.OrientationStr = "vertical",
        force_width: bool = True,
        **kwargs,
    ):
        super().__init__(text, **kwargs)
        self.force_width = force_width
        self.orientation = None
        self._size_hint = None
        self.setOrientation(orientation)

    def setOrientation(self, o: constants.Orientation | constants.OrientationStr):
        o = constants.ORIENTATION.get_enum_value(o)
        if self.orientation == o:
            return
        self.orientation = o
        if o == constants.VERTICAL:
            self.set_min_width(0)
            self.set_max_height(None)
        else:
            self.set_min_width(0)
            self.set_max_width(None)
        self.update()
        self.updateGeometry()

    def paintEvent(self, ev):
        with gui.Painter(self) as p:
            if self.orientation == constants.VERTICAL:
                p.rotate(-90)
                rgn = core.QRect(-self.height(), 0, self.height(), self.width())
            else:
                rgn = self.contentsRect()
            align = self.alignment()
            self._size_hint = p.drawText(rgn, align, self.text())

        if self.orientation == constants.VERTICAL:
            self.setMaximumWidth(self._size_hint.height())
            self.setMinimumHeight(self._size_hint.width() if self.force_width else 0)
        else:
            self.setMaximumHeight(self._size_hint.height())
            self.setMinimumWidth(self._size_hint.width() if self.force_width else 0)

    def sizeHint(self):
        if self.orientation == constants.VERTICAL:
            if self._size_hint:
                return core.QSize(self._size_hint.height(), self._size_hint.width())
            else:
                return core.QSize(19, 50)
        else:
            if self._size_hint:
                return core.QSize(self._size_hint.width(), self._size_hint.height())
            else:
                return core.QSize(50, 19)


if __name__ == "__main__":
    app = widgets.app()
    widget = VerticalLabel("tefsdfsdfsdfsdfsdfst", tool_tip="testus")
    widget.show()
    with app.debug_mode():
        app.exec()
