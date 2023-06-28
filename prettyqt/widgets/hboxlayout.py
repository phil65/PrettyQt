from __future__ import annotations

from prettyqt import widgets


class HBoxLayout(widgets.boxlayout.BoxLayoutMixin, widgets.QHBoxLayout):
    ID = "horizontal"


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    layout = HBoxLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout.add(widget2)
    widget.set_layout(layout)
    widget.show()
    app.exec()
