# -*- coding: utf-8 -*-

import contextlib

from qtpy import QtCore

from prettyqt import core


QtCore.QBuffer.__bases__ = (core.IODevice,)


class Buffer(QtCore.QBuffer):
    @contextlib.contextmanager
    def open_file(self, flag):
        if flag in core.iodevice.OPEN_MODES:
            flag = core.iodevice.OPEN_MODES[flag]
        self.open(flag)
        yield None
        self.close()
