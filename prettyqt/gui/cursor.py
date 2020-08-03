# -*- coding: utf-8 -*-

from typing import Dict, Any

from qtpy import QtCore, QtGui

from prettyqt.utils import bidict, InvalidParamError


SHAPES = bidict(
    arrow=QtCore.Qt.ArrowCursor,
    uparrow=QtCore.Qt.UpArrowCursor,
    cross=QtCore.Qt.CrossCursor,
    wait=QtCore.Qt.WaitCursor,
    caret=QtCore.Qt.IBeamCursor,
)


class Cursor(QtGui.QCursor):
    def serialize_fields(self) -> Dict[str, Any]:
        return dict(shape=self.get_shape(),)

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
        return SHAPES.inv[self.shape()]
