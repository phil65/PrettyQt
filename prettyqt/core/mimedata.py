from typing import Any, Dict, Iterator, List, Union

import orjson as json
from qtpy import QtCore

from prettyqt import core


JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


QtCore.QMimeData.__bases__ = (core.Object,)
OPTS = json.OPT_NAIVE_UTC | json.OPT_SERIALIZE_NUMPY


class MimeData(QtCore.QMimeData):
    def __len__(self):
        return len(self.formats())

    def __getitem__(self, index: str) -> str:
        return self.get_data(index)

    def __setitem__(self, index: str, value: Union[QtCore.QByteArray, bytes, str]):
        if isinstance(value, str):
            value = value.encode()
        if not isinstance(value, QtCore.QByteArray):
            value = QtCore.QByteArray(value)
        self.setData(index, value)

    def __contains__(self, fmt: str):
        return self.hasFormat(fmt)

    def __delitem__(self, index: str):
        self.removeFormat(index)

    def set_data(self, mime_type: str, data: str):
        self.setData(mime_type, QtCore.QByteArray(data.encode()))

    def set_json_data(self, mime_type: str, data: JSONType):
        self.setData(mime_type, QtCore.QByteArray(json.dumps(data, option=OPTS)))

    def get_data(self, mime_type: str) -> str:
        return bytes(self.data(mime_type)).decode()

    def get_json_data(self, mime_type: str) -> JSONType:
        data = self.data(mime_type)
        return json.loads(bytes(data))

    def keys(self) -> List[str]:
        return self.formats()

    def values(self) -> Iterator[Any]:
        return (self.get_data(key) for key in self.formats())
