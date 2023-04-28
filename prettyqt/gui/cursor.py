from __future__ import annotations

from prettyqt import constants, core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, serializemixin


class Cursor(serializemixin.SerializeMixin, QtGui.QCursor):
    @classmethod
    def fake_mouse_move(cls):
        cls.setPos(cls.pos() + core.Point(0, 1))
        gui.Application.processEvents()
        cls.setPos(cls.pos() - core.Point(0, 1))

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
