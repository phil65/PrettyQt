# -*- coding: utf-8 -*-
"""
"""

import contextlib

from qtpy import QtCore

from prettyqt import core


OPEN_MODES = core.iodevice.OPEN_MODES  # type: ignore

QtCore.QBuffer.__bases__ = (core.IODevice,)


class Buffer(QtCore.QBuffer):
    @contextlib.contextmanager
    def open_file(self, flag):
        if flag in OPEN_MODES:
            flag = OPEN_MODES[flag]
        self.open(flag)
        yield None
        self.close()
