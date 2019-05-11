# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from qtpy import QtCore

FORMATS = dict(native=QtCore.QSettings.NativeFormat,
               ini=QtCore.QSettings.IniFormat)

SCOPES = dict(user=QtCore.QSettings.UserScope,
              system=QtCore.QSettings.SystemScope)


class Settings(QtCore.QSettings):

    def __init__(self, *args, settings_id=None):
        self.settings_id = settings_id
        super().__init__(*args)

    def __enter__(self):
        if self.settings_id:
            self.beginGroup(self.settings_id)
        return self

    def __contains__(self, key) -> bool:
        return self.contains(key)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.settings_id:
            self.endGroup()

    def __getitem__(self, index: str):
        return self.value(index)

    def __setitem__(self, name: str, value):
        return self.setValue(name, value)

    @classmethod
    def from_dict(cls, dict: dict):
        settings = cls()
        for k, v in dict.items():
            settings.set_value(k, v)
        return settings

    def set_value(self, key: str, value):
        if not self.applicationName():
            raise ValueError("no app name defined")
        self.setValue(key, value)

    def value(self, key: str, default=None):
        return super().value(key, default)

    @classmethod
    def set_default_format(cls, fmt: str):
        if fmt not in FORMATS:
            raise ValueError("Format must be either 'native' or 'ini'")
        cls.setDefaultFormat(FORMATS[fmt])

    @classmethod
    def set_path(cls, fmt, scope: str, path: str):
        if fmt not in FORMATS:
            raise ValueError("Format must be either 'native' or 'ini'")
        if scope not in SCOPES:
            raise ValueError("Format must be either 'user' or 'system'")
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


if __name__ == "__main__":
    settings = Settings("1", "2")
