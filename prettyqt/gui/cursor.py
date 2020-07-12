# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtGui

from prettyqt.utils import bidict


SHAPES = bidict(
    arrow=QtCore.Qt.ArrowCursor,
    uparrow=QtCore.Qt.UpArrowCursor,
    cross=QtCore.Qt.CrossCursor,
    wait=QtCore.Qt.WaitCursor,
    caret=QtCore.Qt.IBeamCursor,
)


class Cursor(QtGui.QCursor):
    def set_shape(self, shape: str):
        """sets cursor shape

        Allowed values are "arrow", "uparrow", "cross", "wait", "caret"

        Args:
            shape: shape to use

        Raises:
            ValueError: shape does not exist
        """
        if shape not in SHAPES:
            raise ValueError(f"Invalid shape type '{shape}.")
        self.setShape(SHAPES[shape])

    def get_shape(self) -> str:
        """returns current cursor shape

        Possible values: "arrow", "uparrow", "cross", "wait", "caret"

        Returns:
            cursor shape
        """
        return SHAPES.inv[self.shape()]
