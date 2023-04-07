from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class SizeGrip(widgets.WidgetMixin, QtWidgets.QSizeGrip):
    pass


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    widget = SizeGrip(w)
    widget.show()
    app.main_loop()
