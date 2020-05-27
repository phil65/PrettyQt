# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import json

from qtpy import QtCore

from prettyqt import core

QtCore.QMimeData.__bases__ = (core.Object,)


class MimeData(QtCore.QMimeData):

    def set_data(self, mime_type: str, data: str):
        self.setData(mime_type, QtCore.QByteArray(data.encode()))

    def set_json_data(self, mime_type: str, data):
        self.set_data(mime_type, json.dumps(data))

    def get_data(self, mime_type: str) -> str:
        return bytes(self.data(mime_type)).decode()

    def get_json_data(self, mime_type: str):
        data = self.get_data(mime_type)
        return json.loads(data)
