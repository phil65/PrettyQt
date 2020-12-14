from typing import Dict, Any, Literal

from qtpy import QtCore, QtGui

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


SHAPE = bidict(
    arrow=QtCore.Qt.ArrowCursor,
    up_arrow=QtCore.Qt.UpArrowCursor,
    cross=QtCore.Qt.CrossCursor,
    wait=QtCore.Qt.WaitCursor,
    caret=QtCore.Qt.IBeamCursor,
)

ShapeStr = Literal["arrow", "up_arrow", "cross", "wait", "caret"]


class Cursor(QtGui.QCursor):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        super().__init__()
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def serialize_fields(self) -> Dict[str, Any]:
        return dict(shape=self.get_shape())

    def set_shape(self, shape: ShapeStr):
        """Set cursor shape.

        Args:
            shape: shape to use

        Raises:
            InvalidParamError: shape does not exist
        """
        if shape not in SHAPE:
            raise InvalidParamError(shape, SHAPE)
        self.setShape(SHAPE[shape])

    def get_shape(self) -> ShapeStr:
        """Return current cursor shape.

        Returns:
            cursor shape
        """
        return SHAPE.inverse[self.shape()]
