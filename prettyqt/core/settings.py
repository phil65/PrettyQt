# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from qtpy import QtCore

FORMATS = dict(native=QtCore.QSettings.NativeFormat,
               ini=QtCore.QSettings.IniFormat)


class Settings(QtCore.QSettings):

    def __init__(self, settings_id=None):
        self.settings_id = settings_id
        super().__init__()

    def __enter__(self):
        if self.settings_id:
            self.beginGroup(self.settings_id)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.settings_id:
            self.endGroup()

    @staticmethod
    def set_default_format(fmt):
        if fmt not in FORMATS:
            raise ValueError("Format must be either 'native' or 'ini'")
        QtCore.QSettings.setDefaultFormat(FORMATS[fmt])

    @contextlib.contextmanager
    def group(self, prefix):
        self.beginGroup(prefix)
        yield None
        self.endGroup()

    @contextlib.contextmanager
    def write_array(self, prefix, size=-1):
        self.beginWriteArray(prefix, size)
        yield None
        self.endArray()

    @contextlib.contextmanager
    def read_array(self, prefix):
        self.beginReadArray(prefix)
        yield None
        self.endArray()
