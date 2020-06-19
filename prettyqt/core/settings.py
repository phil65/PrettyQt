# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from prettyqt import core
from prettyqt.utils import bidict
from qtpy import QtCore

FORMATS = bidict(native=QtCore.QSettings.NativeFormat,
                 ini=QtCore.QSettings.IniFormat)

SCOPES = bidict(user=QtCore.QSettings.UserScope,
                system=QtCore.QSettings.SystemScope)


QtCore.QSettings.__bases__ = (core.Object,)


class Settings(QtCore.QSettings):

    def __repr__(self):
        return f"Settings: {self.as_dict()}"

    def __init__(self, *args, settings_id=None):
        super().__init__(*args)
        self.settings_id = settings_id

    def __contains__(self, key) -> bool:
        return self.contains(key)

    def __enter__(self):
        if self.settings_id:
            self.beginGroup(self.settings_id)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.settings_id:
            self.endGroup()

    def __getitem__(self, index: str):
        return self.value(index)

    def __setitem__(self, name: str, value):
        return self.setValue(name, value)

    def __delitem__(self, index: str):
        return self.remove(index)

    def __iter__(self):
        return iter(self.allKeys())

    def __len__(self):
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
        self.setValue(key, value)

    def value(self, key: str, default=None):
        return super().value(key, default)

    @classmethod
    def set_default_format(cls, fmt: str):
        """sets the default format

        possible values are "native", "ini"

        Args:
            mode: the default format to use

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
    def set_path(cls, fmt, scope: str, path: str):
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
            raise ValueError(f"Invalid scape. Valid values: {SCOPES.keys()}")
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

    def get(self, key, default=None):
        return super().value(key, default)

    def setdefault(self, key, default=None):
        if not self.contains(key):
            self.set_value(key, default)
        return self

    def keys(self):
        return self.allKeys()

    def values(self):
        return (self.value(key) for key in self.allKeys())

    def items(self):
        return zip(self.keys(), self.values())

    def pop(self, key, default=None):
        if self.contains(key):
            return self.value(key)
        elif default is not None:
            return default
        raise KeyError("Value not set.")

    def popitem(self):
        key = self.keys()[0]
        return (key, self.value(key))

    def update(self, other):
        for k, v in other.items():
            self.set_value(k, v)


if __name__ == "__main__":
    settings = Settings("1", "2")
    settings["1"] = "hallo"
    del settings["hallo"]
