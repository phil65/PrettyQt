# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class MimeData(QtCore.QMimeData):

    def set_data(self, mime_type, data):
        self.setData(mime_type, QtCore.QByteArray(data.encode()))
