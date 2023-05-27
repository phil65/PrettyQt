from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class VBoxLayout(widgets.boxlayout.BoxLayoutMixin, QtWidgets.QVBoxLayout):
    ID = "vertical"


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    layout = VBoxLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout.add(widget2)
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
