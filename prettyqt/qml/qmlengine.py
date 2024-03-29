from __future__ import annotations

import os
import pathlib
from typing import Literal

from prettyqt import core, qml
from prettyqt.utils import bidict, datatypes


ObjectOwnershipStr = Literal["cpp", "javascript"]


OBJECT_OWNERSHIP: bidict[ObjectOwnershipStr, qml.QQmlEngine.ObjectOwnership] = bidict(
    cpp=qml.QQmlEngine.ObjectOwnership.CppOwnership,
    javascript=qml.QQmlEngine.ObjectOwnership.JavaScriptOwnership,
)


class QmlEngineMixin(qml.JSEngineMixin):
    def set_object_ownership(
        self,
        obj: core.QObject,
        mode: ObjectOwnershipStr | qml.QQmlEngine.ObjectOwnership,
    ):
        """Set the object ownership.

        Args:
            obj: object to set ownership for
            mode: object ownership to use
        """
        self.setObjectOwnership(obj, OBJECT_OWNERSHIP.get_enum_value(mode))

    def get_object_ownership(self, obj: core.QObject) -> ObjectOwnershipStr:
        """Return object ownership.

        Returns:
            object ownership
        """
        return OBJECT_OWNERSHIP.inverse[self.objectOwnership(obj)]

    def add_import_path(self, path: datatypes.PathType):
        self.addImportPath(os.fspath(path))

    def add_plugin_path(self, path: datatypes.PathType):
        self.addPluginPath(os.fspath(path))

    def get_plugin_paths(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.pluginPathList()]

    def get_import_paths(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.importPathList()]

    def set_base_url(self, url: str | core.QUrl):
        if isinstance(url, str):
            url = core.QUrl(url)
        self.setBaseUrl(url)

    def get_base_url(self) -> core.Url:
        return core.Url(self.baseUrl())

    def set_offline_storage_path(self, path: datatypes.PathType):
        self.setOfflineStoragePath(os.fspath(path))


class QmlEngine(QmlEngineMixin, qml.QQmlEngine):
    """Environment for instantiating QML components."""
