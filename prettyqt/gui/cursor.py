from __future__ import annotations

from typing import Any

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError


class Cursor(QtGui.QCursor):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        super().__init__()
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def serialize_fields(self) -> dict[str, Any]:
        return dict(shape=self.get_shape())

    def set_shape(self, shape: constants.CursorShapeStr):
        """Set cursor shape.

        Args:
            shape: shape to use

        Raises:
            InvalidParamError: shape does not exist
        """
        if shape not in constants.CURSOR_SHAPE:
            raise InvalidParamError(shape, constants.CURSOR_SHAPE)
        self.setShape(constants.CURSOR_SHAPE[shape])

    def get_shape(self) -> constants.CursorShapeStr:
        """Return current cursor shape.

        Returns:
            cursor shape
        """
        return constants.CURSOR_SHAPE.inverse[self.shape()]

    @classmethod
    def get_position(cls) -> core.Point:
        return core.Point(cls.pos())
