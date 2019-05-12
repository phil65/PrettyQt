# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore

SHAPES = dict(arrow=QtCore.Qt.ArrowCursor,
              uparrow=QtCore.Qt.ArrowCursor,
              cross=QtCore.Qt.CrossCursor,
              wait=QtCore.Qt.WaitCursor,
              caret=QtCore.Qt.IBeamCursor)


class Cursor(QtGui.QCursor):

    def set_shape(self, shape: str):
        self.setShape(SHAPES[shape])
