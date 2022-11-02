from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import helpers, types


QtCore.QMimeData.__bases__ = (core.Object,)


class MimeData(QtCore.QMimeData):
    def __len__(self):
        return len(self.formats())

    def __getitem__(self, index: str) -> str:
        return self.get_data(index)

    def __setitem__(self, index: str, value: types.ByteArrayType):
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

    def set_json_data(self, mime_type: str, data: types.JSONType):
        self.setData(mime_type, QtCore.QByteArray(helpers.dump_json(data)))

    def get_data(self, mime_type: str) -> str:
        return bytes(self.data(mime_type)).decode()

    def get_json_data(self, mime_type: str) -> types.JSONType:
        data = self.data(mime_type)
        return helpers.load_json(bytes(data))

    def keys(self) -> list[str]:
        return self.formats()

    def values(self) -> Iterator[Any]:
        return (self.get_data(key) for key in self.formats())

    def set_svg_data(self, string: str):
        data = string.encode()
        self.setData("image/svg+xml", data)

    def set_path_data(self, paths: list[types.PathType]):
        urls = [core.Url.from_local_file(p) for p in paths]
        self.setUrls(urls)


if __name__ == "__main__":
    mime_data = MimeData()
