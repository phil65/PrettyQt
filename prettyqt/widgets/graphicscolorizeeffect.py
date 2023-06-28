from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import colors, datatypes


class GraphicsColorizeEffect(
    widgets.GraphicsEffectMixin, widgets.QGraphicsColorizeEffect
):
    def set_color(self, color: datatypes.ColorType):
        color = colors.get_color(color)
        super().setColor(color)


if __name__ == "__main__":
    app = widgets.app()
    effect = GraphicsColorizeEffect()
    effect.set_color("window_role")
    print(effect.color())
