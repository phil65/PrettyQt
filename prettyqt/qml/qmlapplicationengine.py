from __future__ import annotations

from collections.abc import Iterator
import os

from prettyqt import core, qml
from prettyqt.qt import QtCore, QtQml
from prettyqt.utils import datatypes


class QmlApplicationEngine(qml.QmlEngineMixin, QtQml.QQmlApplicationEngine):
    def __iter__(self) -> Iterator[QtCore.QObject]:
        return iter(self.rootObjects())

    def load_data(
        self,
        data: datatypes.ByteArrayType,
        url: datatypes.UrlType | None = None,
    ):
        if isinstance(data, str):
            data = data.encode()
        if isinstance(data, bytes):
            data = QtCore.QByteArray(data)
        if isinstance(url, str):
            url = core.Url.from_user_input(url)
        elif url is None:
            url = core.Url()
        self.loadData(data, url)

    def load_file(self, file: datatypes.UrlType | datatypes.PathType):
        if isinstance(file, os.PathLike):
            file = os.fspath(file)
        self.load(file)
