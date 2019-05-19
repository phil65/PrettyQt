# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class MimeData(QtCore.QMimeData):

    def set_data(self, mime_type, data):
        self.setData(mime_type, QtCore.QByteArray(data.encode()))


MimeData.__bases__[0].__bases__ = (core.Object,)
