from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QWidgetItem.__bases__ = (widgets.LayoutItem,)


class WidgetItem(QtWidgets.QWidgetItem):
    pass


if __name__ == "__main__":
    item = WidgetItem(QtWidgets.QWidget())
