from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class GraphicsColorizeEffect(
    widgets.GraphicsEffectMixin, QtWidgets.QGraphicsColorizeEffect
):
    def __setstate__(self, state):
        super().__setstate__(state)
        self.setStrength(state["strength"])
        self.setColor(state["color"])
