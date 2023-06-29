from __future__ import annotations

from prettyqt import gui, widgets


class GraphicsOpacityEffect(widgets.GraphicsEffectMixin, widgets.QGraphicsOpacityEffect):
    def get_opacity_mask(self) -> gui.Brush:
        return gui.Brush(self.opacityMask())
