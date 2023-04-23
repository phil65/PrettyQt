from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets


class GraphicsOpacityEffect(
    widgets.GraphicsEffectMixin, QtWidgets.QGraphicsOpacityEffect
):
    def get_opacity_mask(self) -> gui.Brush:
        return gui.Brush(self.opacityMask())
