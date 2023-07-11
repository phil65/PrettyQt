from __future__ import annotations

from prettyqt import widgets


class WidgetItem(widgets.LayoutItemMixin, widgets.QWidgetItem):
    """Layout item that represents a widget."""


if __name__ == "__main__":
    app = widgets.app()
    item = WidgetItem(widgets.QWidget())
