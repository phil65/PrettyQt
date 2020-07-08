# -*- coding: utf-8 -*-
"""
"""

import orjson as json
from qtpy import QtCore

from prettyqt import core


QtCore.QMimeData.__bases__ = (core.Object,)
OPTS = json.OPT_NAIVE_UTC | json.OPT_SERIALIZE_NUMPY


class MimeData(QtCore.QMimeData):
    def set_data(self, mime_type: str, data: str):
        self.setData(mime_type, QtCore.QByteArray(data.encode()))

    def set_json_data(self, mime_type: str, data):
        self.setData(mime_type, QtCore.QByteArray(json.dumps(data, option=OPTS)))

    def get_data(self, mime_type: str) -> str:
        return bytes(self.data(mime_type)).decode()

    def get_json_data(self, mime_type: str):
        data = self.data(mime_type)
        return json.loads(bytes(data))
