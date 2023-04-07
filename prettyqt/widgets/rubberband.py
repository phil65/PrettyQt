from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


SHAPE = bidict(
    line=QtWidgets.QRubberBand.Shape.Line, rectangle=QtWidgets.QRubberBand.Shape.Rectangle
)

ShapeStr = Literal["line", "rectangle"]


class RubberBandMixin(widgets.WidgetMixin):
    def __init__(
        self,
        shape: ShapeStr | QtWidgets.QRubberBand.Shape,
        parent: QtWidgets.QWidget | None = None,
    ):
        shape = SHAPE[shape] if isinstance(shape, str) else shape
        super().__init__(shape, parent)

    def get_shape(self) -> ShapeStr:
        return SHAPE.inverse[self.shape()]


class RubberBand(RubberBandMixin, QtWidgets.QRubberBand):
    pass
