from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class WidgetItem(widgets.LayoutItemMixin, QtWidgets.QWidgetItem):
    pass


if __name__ == "__main__":
    app = widgets.app()
    item = WidgetItem(QtWidgets.QWidget())
    print(item.get_expanding_directions())
