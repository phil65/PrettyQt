from __future__ import annotations

from collections.abc import Iterator
import os

from prettyqt import qml
from prettyqt.qt import QtCore, QtQml
from prettyqt.utils import datatypes


class QmlApplicationEngine(qml.QmlEngineMixin, QtQml.QQmlApplicationEngine):
    def __iter__(self) -> Iterator[QtCore.QObject]:
        return iter(self.rootObjects())

    def load_data(
        self,
        data: datatypes.ByteArrayType,
        url: datatypes.UrlType | os.PathLike | None = None,
    ):
        data = datatypes.to_bytearray(data)
        url = datatypes.to_local_url(url)
        self.loadData(data, url)

    def load_file(self, file: datatypes.UrlType | datatypes.PathType):
        if isinstance(file, os.PathLike):
            file = os.fspath(file)
        self.load(file)
