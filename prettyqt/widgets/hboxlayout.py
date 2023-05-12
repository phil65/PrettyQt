from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class HBoxLayout(widgets.boxlayout.BoxLayoutMixin, QtWidgets.QHBoxLayout):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        margin: int | None = None,
    ):
        QtWidgets.QHBoxLayout.__init__(self)
        widgets.LayoutMixin.__init__(self)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    layout = HBoxLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout.add(widget2)
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
