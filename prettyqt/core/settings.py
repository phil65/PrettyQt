import contextlib
import logging
import pathlib
from typing import Any, Dict, Iterator, List, Literal, Mapping, Optional, Tuple, Union

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


logger = logging.getLogger(__name__)

FORMAT = bidict(native=QtCore.QSettings.NativeFormat, ini=QtCore.QSettings.IniFormat)

FormatStr = Literal["user", "system"]

SCOPE = bidict(user=QtCore.QSettings.UserScope, system=QtCore.QSettings.SystemScope)

ScopeStr = Literal["user", "system"]

QtCore.QSettings.__bases__ = (core.Object,)


class Settings(QtCore.QSettings):
    def __init__(self, *args, settings_id: Optional[str] = None):
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

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self.items())

    def __len__(self) -> int:
        return len(self.allKeys())

    @classmethod
    def build_from_dict(cls, dct: Dict[str, Any]):
        settings = cls()
        for k, v in dct.items():
            settings.set_value(k, v)
        return settings

    def as_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.items()}

    def set_value(self, key: str, value):
        if not self.applicationName():
            raise RuntimeError("no app name defined")
        self.setValue(key, dict(value=value))

    def set_values(self, dct: Dict[str, Any]):
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
    def set_path(cls, fmt: FormatStr, scope: ScopeStr, path: Union[str, pathlib.Path]):
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
        cls.setPath(FORMAT[fmt], SCOPE[scope], str(path))

    @contextlib.contextmanager
    def group(self, prefix: str):
        """Context manager for setting groups.

        Args:
            prefix: setting prefix for group
        """
        self.beginGroup(prefix)
        yield None
        self.endGroup()

    @contextlib.contextmanager
    def write_array(self, prefix: str, size: int = -1):
        """Context manager for writing arrays.

        Args:
            prefix: prefix for settings array
            size: size of settings array
        """
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

    def keys(self) -> List[str]:
        return self.allKeys()

    def values(self) -> Iterator[Any]:
        return (self.get_value(key) for key in self.allKeys())

    def items(self):
        return zip(self.keys(), self.values())

    def pop(self, key: str):
        if self.contains(key):
            return self.get_value(key)
        raise KeyError(key)

    def popitem(self) -> Tuple[str, Any]:
        key = self.keys()[0]
        return (key, self.get_value(key))

    def update(self, other: Mapping):
        for k, v in other.items():
            self.set_value(k, v)


def register_extensions(
    *exts: str,
    app_name: Optional[str] = None,
    app_path: Union[None, str, pathlib.Path] = None,
):
    logger.debug(f"assigning extensions {exts} to {app_name}")
    s = Settings("HKEY_CURRENT_USER\\SOFTWARE\\Classes", Settings.NativeFormat)
    if app_path is None:
        app_path = str(core.CoreApplication.get_application_file_path())
    if app_name is None:
        app_name = core.CoreApplication.applicationName()
    for ext in exts:
        s.setValue(f"{ext}/DefaultIcon/.", app_path)  # perhaps ,0 after app_path
        s.setValue(f"{ext}/.", app_name)
    s.setValue(f"{app_name}/shell/open/command/.", f"{app_path} %1")


if __name__ == "__main__":
    settings = Settings("1", "2")
    settings["1"] = True
    print(settings["1"])
    print(type(settings.get("1")))
    del settings["hallo"]
