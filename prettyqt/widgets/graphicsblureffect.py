from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


BlurHintStr = Literal["performance", "quality", "animation"]

BLUR_HINTS: bidict[BlurHintStr, QtWidgets.QGraphicsBlurEffect.BlurHint] = bidict(
    performance=QtWidgets.QGraphicsBlurEffect.BlurHint.PerformanceHint,
    quality=QtWidgets.QGraphicsBlurEffect.BlurHint.QualityHint,
    animation=QtWidgets.QGraphicsBlurEffect.BlurHint.AnimationHint,
)


class GraphicsBlurEffect(widgets.GraphicsEffectMixin, QtWidgets.QGraphicsBlurEffect):
    def set_blur_hints(self, *hints: BlurHintStr):
        for item in hints:
            if item not in BLUR_HINTS:
                raise InvalidParamError(item, BLUR_HINTS)
        if hints:
            flags = BLUR_HINTS.merge_flags(hints)
        else:
            flags = QtWidgets.QGraphicsBlurEffect.BlurHint(0)  # type: ignore
        self.setBlurHints(flags)

    def get_blur_hints(self) -> list[BlurHintStr]:
        return BLUR_HINTS.get_list(self.blurHints())
