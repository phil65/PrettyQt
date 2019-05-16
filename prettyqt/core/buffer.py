# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from qtpy import QtCore

from prettyqt import core


class Buffer(QtCore.QBuffer):
    @contextlib.contextmanager
    def open_file(self, flags):
        self.open(flags)
        yield None
        self.close()


Buffer.__bases__[0].__bases__ = (core.IODevice,)
