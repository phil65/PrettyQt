# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtMultimedia

from prettyqt import core


QtMultimedia.QMediaControl.__bases__ = (core.Object,)


class MediaControl(QtMultimedia.QMediaControl):
    pass
