from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class FocusFrame(widgets.WidgetMixin, QtWidgets.QFocusFrame):
    pass


if __name__ == "__main__":
    app = widgets.app()
    container = widgets.Splitter()
    widget = widgets.PlainTextEdit()
    widget2 = widgets.PlainTextEdit()
    container.add(widget)
    container.add(widget2)
    errorbox = FocusFrame(container)
    errorbox.setWidget(container)
    errorbox.show()
    container.show()
    app.main_loop()
