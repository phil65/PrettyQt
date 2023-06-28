from __future__ import annotations

from prettyqt import widgets


class VBoxLayout(widgets.boxlayout.BoxLayoutMixin, widgets.QVBoxLayout):
    ID = "vertical"


if __name__ == "__main__":
    app = widgets.app()
    layout = VBoxLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout.add(widget2)
    widget.set_layout(layout)
    widget.show()
    app.exec()
