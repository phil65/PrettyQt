from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class WidgetItemMixin:
    pass


class WidgetItem(WidgetItemMixin, QtWidgets.QWidgetItem, widgets.LayoutItem):
    pass


if __name__ == "__main__":
    item = WidgetItem(QtWidgets.QWidget())
