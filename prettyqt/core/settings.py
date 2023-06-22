from __future__ import annotations

from collections.abc import Iterator, Mapping, MutableMapping, Sequence
import contextlib
import logging
import os
import sys
from typing import Any, Literal

from typing_extensions import Self

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, datatypes


logger = logging.getLogger(__name__)

FormatStr = Literal["user", "system"]

FORMAT: bidict[FormatStr, QtCore.QSettings.Format] = bidict(
    native=QtCore.QSettings.Format.NativeFormat, ini=QtCore.QSettings.Format.IniFormat
)

ScopeStr = Literal["user", "system"]

SCOPE: bidict[ScopeStr, QtCore.QSettings.Scope] = bidict(
    user=QtCore.QSettings.Scope.UserScope, system=QtCore.QSettings.Scope.SystemScope
)


class Settings_(
    core.ObjectMixin, QtCore.QSettings, MutableMapping, metaclass=datatypes.QABCMeta
):
    # Setting class with original behavior, compatible with original QSettings
    def __init__(self, *args, settings_id: str | None = None):
        super().__init__(*args)
        self.settings_id = settings_id

    def __repr__(self):
        return f"{type(self).__name__}({dict(self)})"

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
        if index not in self.allKeys():
            raise KeyError(index)
        return self.get_value(index)

    def __setitem__(self, name: str, value):
        return self.set_value(name, value)

    def __delitem__(self, key: str):
        if not self.contains(key):
            raise KeyError(key)
        return self.remove(key)

    def __iter__(self) -> Iterator[str]:
        return iter(self.allKeys())

    def __len__(self) -> int:
        return len(self.allKeys())

    def __ior__(self, other: Mapping):
        self.update(other)
        return self

    def set_value(self, key: str, value):
        if not self.applicationName():
            raise RuntimeError("no app name defined")
        if isinstance(value, Settings_):
            value = dict(value)
        self.setValue(key, value)

    def get_value(self, key: str, default=None):
        return self.value(key) if self.contains(key) else default

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
    def set_path(cls, fmt: FormatStr, scope: ScopeStr, path: datatypes.PathType):
        """Set the path to the settings file.

        Args:
            fmt: the default format to use
            scope: the scope to use
            path: the path to set

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

    def write_array(self, prefix: str, array: Sequence) -> Iterator[tuple[Self, Any]]:
        """Context manager for writing arrays.

        Args:
            prefix: prefix for settings array
            array: array used to write settings

        Returns:
            Iterator yielding (setting, arrayitem) items
        """
        self.beginWriteArray(prefix, len(array))
        for i, _ in enumerate(array):
            self.setArrayIndex(i)
            yield (self, array[i])
        self.endArray()

    def read_array(self, prefix: str) -> Iterator[Settings_]:
        """Context manager for reading arrays.

        Args:
            prefix: prefix for settings array
        """
        size = self.beginReadArray(prefix)
        for i in range(size):
            self.setArrayIndex(i)
            yield self
        self.endArray()

    # MutableMapping overrides

    def keys(self) -> list[str]:
        return self.allKeys()

    def setdefault(self, key: str, default: Any = None) -> Any:
        if not self.contains(key):
            self.set_value(key, default)
            return default
        return self.get_value(key)

    @classmethod
    def register_extensions(
        cls,
        *exts: str,
        app_name: str | None = None,
        app_path: None | datatypes.PathType = None,
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
        if getattr(sys, "frozen", False):
            s.setValue(f"{app_name}/shell/open/command/.", f"{app_path} %1")
        else:
            command_value = rf'{sys.executable} -m {app_path} "%V"'
            s.setValue(f"{app_name}/shell/open/command/.", f"{command_value} %1")


class Settings(Settings_):
    """Settings class which wraps everything into a dict to preserve data types."""
    def set_value(self, key: str, value):
        match value:
            case Settings_():
                setting = dict(value=dict(value), typ="subsetting")
            case _:
                setting = dict(value=value, typ="regular")
        super().set_value(key, setting)

    def get_value(self, key: str, default=None):
        if not self.contains(key):
            return default
        val = self.value(key)
        # TODO: convert settings dicts back?
        match val:
            case {"value": setting}:
                return setting
            case _:
                # this is for migration
                self.set_value(key, val)
                return val


if __name__ == "__main__":
    settings = Settings("1", "2")
    settings["1"] = True
    settings |= dict(abc="abc")
