import pathlib
from typing import List, Literal, Union

from qtpy import QtCore, QtQml

from prettyqt import qml
from prettyqt.utils import InvalidParamError, bidict


OBJECT_OWNERSHIP = bidict(
    cpp=QtQml.QQmlEngine.CppOwnership,
    javascript=QtQml.QQmlEngine.JavaScriptOwnership,
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

    def add_import_path(self, path: Union[str, pathlib.Path]):
        self.addImportPath(str(path))

    def add_plugin_path(self, path: Union[str, pathlib.Path]):
        self.addPluginPath(str(path))

    def get_plugin_paths(self) -> List[pathlib.Path]:
        return [pathlib.Path(p) for p in self.pluginPathList()]

    def get_import_paths(self) -> List[pathlib.Path]:
        return [pathlib.Path(p) for p in self.importPathList()]
