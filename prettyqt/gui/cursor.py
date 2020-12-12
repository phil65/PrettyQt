from typing import Dict, Any

from qtpy import QtCore, QtGui

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


SHAPES = bidict(
    arrow=QtCore.Qt.ArrowCursor,
    uparrow=QtCore.Qt.UpArrowCursor,
    cross=QtCore.Qt.CrossCursor,
    wait=QtCore.Qt.WaitCursor,
    caret=QtCore.Qt.IBeamCursor,
)


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

    def set_shape(self, shape: str):
        """Set cursor shape.

        Allowed values are "arrow", "uparrow", "cross", "wait", "caret"

        Args:
            shape: shape to use

        Raises:
            InvalidParamError: shape does not exist
        """
        if shape not in SHAPES:
            raise InvalidParamError(shape, SHAPES)
        self.setShape(SHAPES[shape])

    def get_shape(self) -> str:
        """Return current cursor shape.

        Possible values: "arrow", "uparrow", "cross", "wait", "caret"

        Returns:
            cursor shape
        """
        return SHAPES.inverse[self.shape()]
