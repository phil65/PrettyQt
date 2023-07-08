from __future__ import annotations

from prettyqt import widgets


class SizeGrip(widgets.WidgetMixin, widgets.QSizeGrip):
    @classmethod
    def setup_example(cls):
        w = widgets.Widget()
        return cls(w)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    widget = SizeGrip(w)
    widget.show()
    app.exec()
