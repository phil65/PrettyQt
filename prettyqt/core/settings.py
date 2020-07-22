# -*- coding: utf-8 -*-
"""
"""

import contextlib
import pathlib
from typing import List, Mapping, Optional, Union
import logging

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict

logger = logging.getLogger(__name__)

FORMATS = bidict(native=QtCore.QSettings.NativeFormat, ini=QtCore.QSettings.IniFormat)

SCOPES = bidict(user=QtCore.QSettings.UserScope, system=QtCore.QSettings.SystemScope)


QtCore.QSettings.__bases__ = (core.Object,)


class Settings(QtCore.QSettings):
    def __init__(self, *args, settings_id: Optional[str] = None):
        super().__init__(*args)
        self.settings_id = settings_id

    def __repr__(self):
        return f"Settings: {self.as_dict()}"

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

    def __iter__(self):
        return iter(self.allKeys())

    def __len__(self) -> int:
        return len(self.allKeys())

    @classmethod
    def build_from_dict(cls, dct: dict):
        settings = cls()
        for k, v in dct.items():
            settings.set_value(k, v)
        return settings

    def as_dict(self):
        return {k: v for k, v in self.items()}

    def set_value(self, key: str, value):
        if not self.applicationName():
            raise ValueError("no app name defined")
        self.setValue(key, dict(value=value))

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
    def set_default_format(cls, fmt: str):
        """sets the default format

        possible values are "native", "ini"

        Args:
            fmt: the default format to use

        Raises:
            ValueError: invalid format
        """
        if fmt not in FORMATS:
            raise ValueError(f"Invalid value. Valid values: {FORMATS.keys()}")
        cls.setDefaultFormat(FORMATS[fmt])

    @classmethod
    def get_default_format(cls) -> str:
        """returns default settings format

        possible values are "native", "ini"

        Returns:
            default settings format
        """
        return FORMATS.inv[cls.defaultFormat()]

    def get_scope(self) -> str:
        """returns scope

        possible values are "user", "system"

        Returns:
            scope
        """
        return SCOPES.inv[self.scope()]

    @classmethod
    def set_path(cls, fmt: str, scope: str, path: Union[str, pathlib.Path]):
        """sets the path to the settings file

        Args:
            fmt: the default format to use
            scope: the scope to use

        Raises:
            ValueError: invalid format or scope
        """
        if fmt not in FORMATS:
            raise ValueError(f"Invalid format. Valid values: {FORMATS.keys()}")
        if scope not in SCOPES:
            raise ValueError(f"Invalid scope. Valid values: {SCOPES.keys()}")
        cls.setPath(FORMATS[fmt], SCOPES[scope], str(path))

    @contextlib.contextmanager
    def group(self, prefix: str):
        """context manager for setting groups

        Args:
            prefix: setting prefix for group
        """
        self.beginGroup(prefix)
        yield None
        self.endGroup()

    @contextlib.contextmanager
    def write_array(self, prefix: str, size: int = -1):
        """context manager for writing arrays

        Args:
            prefix: prefix for settings array
            size: size of settings array
        """
        self.beginWriteArray(prefix, size)
        yield None
        self.endArray()

    @contextlib.contextmanager
    def read_array(self, prefix: str):
        """context manager for reading arrays

        Args:
            prefix: prefix for settings array
        """
        self.beginReadArray(prefix)
        yield None
        self.endArray()

    # Dictionary interface

    def get(self, key: str, default=None):
        return self.get_value(key, default)

    def setdefault(self, key: str, default=None):
        if not self.contains(key):
            self.set_value(key, default)
            return default
        return self.get_value(key)

    def keys(self) -> List[str]:
        return self.allKeys()

    def values(self):
        return (self.get_value(key) for key in self.allKeys())

    def items(self):
        return zip(self.keys(), self.values())

    def pop(self, key: str):
        if self.contains(key):
            return self.get_value(key)
        raise KeyError(key)

    def popitem(self) -> tuple:
        key = self.keys()[0]
        return (key, self.get_value(key))

    def update(self, other: Mapping):
        for k, v in other.items():
            self.set_value(k, v)


def register_extensions(*exts, app_name=None, app_path=None):
    logger.debug(f"assigning extensions {exts} to {app_name}")
    s = Settings("HKEY_CURRENT_USER\\SOFTWARE\\Classes", Settings.NativeFormat)
    if app_path is None:
        app_path = core.Dir.toNativeSeparators(core.CoreApplication.applicationFilePath())
    if app_name is None:
        app_name = core.CoreApplication.applicationName()
    for ext in exts:
        s.setValue(f"{ext}/DefaultIcon/.", app_path)  # perhaps ,0 after app_path
        s.setValue(f"{ext}/.", app_name)
    s.setValue(f"{app_name}/shell/open/command/.", app_path + " %1")


if __name__ == "__main__":
    settings = Settings("1", "2")
    settings["1"] = True
    print(settings["1"])
    print(type(settings.get("1")))
    del settings["hallo"]
