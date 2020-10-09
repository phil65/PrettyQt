# -*- coding: utf-8 -*-

from typing import Union, List
import pathlib

from qtpy import QtQml, QtCore

from prettyqt import qml
from prettyqt.utils import bidict, InvalidParamError

OBJECT_OWNERSHIPS = bidict(
    cpp=QtQml.QQmlEngine.CppOwnership,
    javascript=QtQml.QQmlEngine.JavaScriptOwnership,
)

QtQml.QQmlEngine.__bases__ = (qml.JSEngine,)


class QmlEngine(QtQml.QQmlEngine):
    def set_object_ownership(self, obj: QtCore.QObject, mode: str):
        """Set the object ownership.

        valid values: "cpp", "javascript"

        Args:
            mode: object ownership to use

        Raises:
            InvalidParamError: invalid object ownership
        """
        if mode not in OBJECT_OWNERSHIPS:
            raise InvalidParamError(mode, OBJECT_OWNERSHIPS)
        self.setObjectOwnership(obj, OBJECT_OWNERSHIPS[mode])

    def get_object_ownership(self, obj: QtCore.QObject) -> str:
        """Return object ownership.

        possible values: "cpp", "javascript"

        Returns:
            object ownership
        """
        return OBJECT_OWNERSHIPS.inv[self.objectOwnership(obj)]

    def add_import_path(self, path: Union[str, pathlib.Path]):
        self.addImportPath(str(path))

    def add_plugin_path(self, path: Union[str, pathlib.Path]):
        self.addPluginPath(str(path))

    def get_plugin_paths(self) -> List[pathlib.Path]:
        return [pathlib.Path(p) for p in self.pluginPathList()]

    def get_import_paths(self) -> List[pathlib.Path]:
        return [pathlib.Path(p) for p in self.importPathList()]
