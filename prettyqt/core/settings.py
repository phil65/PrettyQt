from __future__ import annotations

from collections.abc import Iterator, Mapping
import contextlib
import logging
import os
from typing import Any, Literal

from deprecated import deprecated

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, types


logger = logging.getLogger(__name__)

FORMAT = bidict(
    native=QtCore.QSettings.Format.NativeFormat, ini=QtCore.QSettings.Format.IniFormat
)

FormatStr = Literal["user", "system"]

SCOPE = bidict(
    user=QtCore.QSettings.Scope.UserScope, system=QtCore.QSettings.Scope.SystemScope
)

ScopeStr = Literal["user", "system"]

QtCore.QSettings.__bases__ = (core.Object,)


class Settings(QtCore.QSettings):
    def __init__(self, *args, settings_id: str | None = None):
        super().__init__(*args)
        self.settings_id = settings_id

    def __repr__(self):
        return f"{type(self).__name__}: {self.as_dict()}"

    def __contains__(self, key: str) -> bool:
        return self.contains(key)

    def __enter__(self):
        if self.settings_id:
            self.beginGroup(self.settings_id)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.settings_id:
            self.endGroup()

    def __getitem__(self, index: str):
        return self.get_value(index)

    def __setitem__(self, name: str, value):
        return self.set_value(name, value)

    def __delitem__(self, key: str):
        if not self.contains(key):
            raise KeyError(key)
        return self.remove(key)

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        return iter(self.items())

    def __len__(self) -> int:
        return len(self.allKeys())

    @classmethod
    def build_from_dict(cls, dct: dict[str, Any]):
        settings = cls()
        for k, v in dct.items():
            settings.set_value(k, v)
        return settings

    def as_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.items()}

    def set_value(self, key: str, value):
        if not self.applicationName():
            raise RuntimeError("no app name defined")
        self.setValue(key, dict(value=value))

    def set_values(self, dct: dict[str, Any]):
        for k, v in dct.items():
            self.set_value(k, v)

    def get_value(self, key: str, default=None):
        if not self.contains(key):
            return default
        val = self.value(key)
        # this is for migration
        if not isinstance(val, dict) or "value" not in val:
            self.set_value(key, val)
            return val
        return val["value"]

    @classmethod
    def set_default_format(cls, fmt: FormatStr):
        """Set the default format.

        Args:
            fmt: the default format to use

        Raises:
            InvalidParamError: invalid format
        """
        if fmt not in FORMAT:
            raise InvalidParamError(fmt, FORMAT)
        cls.setDefaultFormat(FORMAT[fmt])

    @classmethod
    def get_default_format(cls) -> FormatStr:
        """Return default settings format.

        Returns:
            default settings format
        """
        return FORMAT.inverse[cls.defaultFormat()]

    def get_scope(self) -> ScopeStr:
        """Return scope.

        Returns:
            scope
        """
        return SCOPE.inverse[self.scope()]

    @classmethod
    def set_path(cls, fmt: FormatStr, scope: ScopeStr, path: types.PathType):
        """Set the path to the settings file.

        Args:
            fmt: the default format to use
            scope: the scope to use

        Raises:
            InvalidParamError: invalid format or scope
        """
        if fmt not in FORMAT:
            raise InvalidParamError(fmt, FORMAT)
        if scope not in SCOPE:
            raise InvalidParamError(scope, SCOPE)
        cls.setPath(FORMAT[fmt], SCOPE[scope], os.fspath(path))

    @contextlib.contextmanager
    def edit_group(self, prefix: str):
        """Context manager for setting groups.

        Args:
            prefix: setting prefix for group
        """
        self.beginGroup(prefix)
        yield None
        self.endGroup()

    @contextlib.contextmanager
    def write_array(self, prefix: str, size: int | None = None):
        """Context manager for writing arrays.

        Args:
            prefix: prefix for settings array
            size: size of settings array
        """
        if size is None:
            size = -1
        self.beginWriteArray(prefix, size)
        yield None
        self.endArray()

    @contextlib.contextmanager
    def read_array(self, prefix: str):
        """Context manager for reading arrays.

        Args:
            prefix: prefix for settings array
        """
        self.beginReadArray(prefix)
        yield None
        self.endArray()

    # Dictionary interface

    def get(self, key: str, default: Any = None) -> Any:
        return self.get_value(key, default)

    def setdefault(self, key: str, default: Any = None) -> Any:
        if not self.contains(key):
            self.set_value(key, default)
            return default
        return self.get_value(key)

    def keys(self) -> list[str]:
        return self.allKeys()

    def values(self) -> Iterator[Any]:
        return (self.get_value(key) for key in self.allKeys())

    def items(self):
        return zip(self.keys(), self.values())

    def pop(self, key: str):
        if self.contains(key):
            return self.get_value(key)
        raise KeyError(key)

    def popitem(self) -> tuple[str, Any]:
        key = self.keys()[0]
        return (key, self.get_value(key))

    def update(self, other: Mapping[str, Any]):
        for k, v in other.items():
            self.set_value(k, v)

    @classmethod
    def register_extensions(
        cls,
        *exts: str,
        app_name: str | None = None,
        app_path: None | types.PathType = None,
    ):
        logger.debug(f"assigning extensions {exts} to {app_name}")
        s = cls("HKEY_CURRENT_USER\\SOFTWARE\\Classes", Settings.Format.NativeFormat)
        if app_path is None:
            app_path = str(core.CoreApplication.get_application_file_path())
        app_path = os.fspath(app_path)
        if app_name is None:
            app_name = core.CoreApplication.applicationName()
        for ext in exts:
            s.setValue(f"{ext}/DefaultIcon/.", app_path)  # perhaps ,0 after app_path
            s.setValue(f"{ext}/.", app_name)
        s.setValue(f"{app_name}/shell/open/command/.", f"{app_path} %1")


@deprecated(reason="This method is deprecated, use Settings.register_extensions instead.")
def register_extensions(
    *exts: str,
    app_name: str | None = None,
    app_path: None | types.PathType = None,
):
    core.Settings.register_extensions(*exts, app_name=app_name, app_path=app_path)


if __name__ == "__main__":
    settings = Settings("1", "2")
    settings["1"] = True
    print(settings["1"])
    print(type(settings.get("1")))
    del settings["hallo"]
