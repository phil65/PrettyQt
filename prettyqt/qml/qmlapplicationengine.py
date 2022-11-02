from __future__ import annotations

from collections.abc import Iterator
import os

from prettyqt import core
from prettyqt.qt import QtCore, QtQml
from prettyqt.utils import types


QtQml.QQmlApplicationEngine.__bases__ = (QtQml.QQmlEngine,)


class QmlApplicationEngine(QtQml.QQmlApplicationEngine):
    def __iter__(self) -> Iterator[QtCore.QObject]:
        return iter(self.rootObjects())

    def load_data(
        self,
        data: types.ByteArrayType,
        url: types.UrlType | None = None,
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

    def load_file(self, file: types.UrlType | types.PathType):
        if isinstance(file, os.PathLike):
            file = os.fspath(file)
        self.load(file)
