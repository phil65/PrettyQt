# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtMultimedia

from prettyqt import core


QtMultimedia.QMediaObject.__bases__ = (core.Object,)


class MediaObject(QtMultimedia.QMediaObject):
    pass
