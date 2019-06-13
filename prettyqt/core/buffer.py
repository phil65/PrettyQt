# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from qtpy import QtCore

from prettyqt import core


QtCore.QBuffer.__bases__ = (core.IODevice,)


class Buffer(QtCore.QBuffer):
    @contextlib.contextmanager
    def open_file(self, flags):
        self.open(flags)
        yield None
        self.close()
