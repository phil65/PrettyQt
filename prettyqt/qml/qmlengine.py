from __future__ import annotations

import os
import pathlib
from typing import Literal

from prettyqt import core, qml
from prettyqt.qt import QtCore, QtQml
from prettyqt.utils import InvalidParamError, bidict, types


OBJECT_OWNERSHIP = bidict(
    cpp=QtQml.QQmlEngine.ObjectOwnership.CppOwnership,
    javascript=QtQml.QQmlEngine.ObjectOwnership.JavaScriptOwnership,
)

ObjectOwnershipStr = Literal["cpp", "javascript"]

QtQml.QQmlEngine.__bases__ = (qml.JSEngine,)


class QmlEngine(QtQml.QQmlEngine):
    def set_object_ownership(self, obj: QtCore.QObject, mode: ObjectOwnershipStr):
        """Set the object ownership.

        Args:
            mode: object ownership to use

        Raises:
            InvalidParamError: invalid object ownership
        """
        if mode not in OBJECT_OWNERSHIP:
            raise InvalidParamError(mode, OBJECT_OWNERSHIP)
        self.setObjectOwnership(obj, OBJECT_OWNERSHIP[mode])

    def get_object_ownership(self, obj: QtCore.QObject) -> ObjectOwnershipStr:
        """Return object ownership.

        Returns:
            object ownership
        """
        return OBJECT_OWNERSHIP.inverse[self.objectOwnership(obj)]

    def add_import_path(self, path: types.PathType):
        self.addImportPath(os.fspath(path))

    def add_plugin_path(self, path: types.PathType):
        self.addPluginPath(os.fspath(path))

    def get_plugin_paths(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.pluginPathList()]

    def get_import_paths(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.importPathList()]

    def set_base_url(self, url: str | QtCore.QUrl):
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        self.setBaseUrl(url)

    def get_base_url(self) -> core.Url:
        return core.Url(self.baseUrl())

    def set_offline_storage_path(self, path: types.PathType):
        self.setOfflineStoragePath(os.fspath(path))
