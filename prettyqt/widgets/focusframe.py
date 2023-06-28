from __future__ import annotations

from prettyqt import widgets


class FocusFrame(widgets.WidgetMixin, widgets.QFocusFrame):
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
    app.exec()
