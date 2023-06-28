from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict


BlurHintStr = Literal["performance", "quality", "animation"]

BLUR_HINTS: bidict[BlurHintStr, widgets.QGraphicsBlurEffect.BlurHint] = bidict(
    performance=widgets.QGraphicsBlurEffect.BlurHint.PerformanceHint,
    quality=widgets.QGraphicsBlurEffect.BlurHint.QualityHint,
    animation=widgets.QGraphicsBlurEffect.BlurHint.AnimationHint,
)


class GraphicsBlurEffect(widgets.GraphicsEffectMixin, widgets.QGraphicsBlurEffect):
    def set_blur_hints(self, *hints: BlurHintStr):
        if hints:
            flags = BLUR_HINTS.merge_flags(hints)
        else:
            flags = widgets.QGraphicsBlurEffect.BlurHint(0)  # type: ignore
        self.setBlurHints(flags)

    def get_blur_hints(self) -> list[BlurHintStr]:
        return BLUR_HINTS.get_list(self.blurHints())
