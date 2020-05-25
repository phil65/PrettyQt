# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core

QtCore.QMimeData.__bases__ = (core.Object,)


class MimeData(QtCore.QMimeData):

    def set_data(self, mime_type: str, data: str):
        self.setData(mime_type, QtCore.QByteArray(data.encode()))

    def get_data(self, mime_type: str):
        return bytes(self.data(mime_type)).decode()
