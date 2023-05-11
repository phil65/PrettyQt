from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtWidgets


class WidgetAction(gui.ActionMixin, QtWidgets.QWidgetAction):
    pass


if __name__ == "__main__":
    w = WidgetAction()
