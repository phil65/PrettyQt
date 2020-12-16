from typing import Optional, Union

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


SHAPE = bidict(line=QtWidgets.QRubberBand.Line, rectangle=QtWidgets.QRubberBand.Rectangle)


QtWidgets.QRubberBand.__bases__ = (widgets.Widget,)


class RubberBand(QtWidgets.QRubberBand):
    def __init__(
        self, shape: Union[str, int], parent: Optional[QtWidgets.QWidget] = None
    ):
        if isinstance(shape, str):
            shape = SHAPE[shape]
        super().__init__(shape, parent)

    def get_shape(self) -> str:
        return SHAPE.inverse[self.shape()]
