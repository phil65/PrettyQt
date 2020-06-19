# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt.utils import bidict
from prettyqt import core


OPEN_MODES = bidict(not_open=QtCore.QIODevice.NotOpen,
                    read_only=QtCore.QIODevice.ReadOnly,
                    write_only=QtCore.QIODevice.WriteOnly,
                    read_write=QtCore.QIODevice.ReadWrite,
                    append=QtCore.QIODevice.Append,
                    truncate=QtCore.QIODevice.Truncate,
                    text=QtCore.QIODevice.Text,
                    unbuffered=QtCore.QIODevice.Unbuffered,
                    new_only=QtCore.QIODevice.NewOnly,
                    existing_only=QtCore.QIODevice.ExistingOnly)

QtCore.QIODevice.__bases__ = (core.Object,)


class IODevice(QtCore.QIODevice):
    pass
