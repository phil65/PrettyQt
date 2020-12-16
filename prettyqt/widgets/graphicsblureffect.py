from typing import List

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import InvalidParamError, bidict, helpers


BLUR_HINTS = bidict(
    performance=QtWidgets.QGraphicsBlurEffect.PerformanceHint,
    quality=QtWidgets.QGraphicsBlurEffect.QualityHint,
    animation=QtWidgets.QGraphicsBlurEffect.AnimationHint,
)


QtWidgets.QGraphicsBlurEffect.__bases__ = (widgets.GraphicsEffect,)


class GraphicsBlurEffect(QtWidgets.QGraphicsBlurEffect):
    def serialize_fields(self):
        return dict(blur_radius=self.blurRadius(), blur_hints=self.get_blur_hints())

    def set_blur_hints(self, *hints: str):
        for item in hints:
            if item not in BLUR_HINTS:
                raise InvalidParamError(item, BLUR_HINTS)
        flags = helpers.merge_flags(hints, BLUR_HINTS)
        self.setBlurHints(flags)

    def get_blur_hints(self) -> List[str]:
        return [k for k, v in BLUR_HINTS.items() if v & self.blurHints()]
