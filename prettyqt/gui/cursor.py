# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore

from prettyqt.utils import bidict


SHAPES = bidict(arrow=QtCore.Qt.ArrowCursor,
                uparrow=QtCore.Qt.UpArrowCursor,
                cross=QtCore.Qt.CrossCursor,
                wait=QtCore.Qt.WaitCursor,
                caret=QtCore.Qt.IBeamCursor)


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
            raise ValueError("Invalid shape type.")
        self.setShape(SHAPES[shape])

    def get_shape(self):
        """returns current cursor shape

        Possible values: "arrow", "uparrow", "cross", "wait", "caret"

        Returns:
            cursor shape
        """
        return SHAPES.inv[self.shape()]
