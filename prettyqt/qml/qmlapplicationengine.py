from __future__ import annotations

import os
from typing import Iterator, Optional, Union

from prettyqt import core
from prettyqt.qt import QtCore, QtQml


QtQml.QQmlApplicationEngine.__bases__ = (QtQml.QQmlEngine,)


class QmlApplicationEngine(QtQml.QQmlApplicationEngine):
    def __iter__(self) -> Iterator[QtCore.QObject]:
        return iter(self.rootObjects())

    def load_data(
        self,
        data: Union[QtCore.QByteArray, bytes, str],
        url: Optional[Union[QtCore.QUrl, str]] = None,
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

    def load_file(self, file: Union[str, os.PathLike, QtCore.QUrl]):
        if isinstance(file, os.PathLike):  # type: ignore
            file = os.fspath(file)
        self.load(file)
