from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QFocusFrame.__bases__ = (widgets.Widget,)


class FocusFrame(QtWidgets.QFocusFrame):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = FocusFrame()
    widget.show()
    app.main_loop()
