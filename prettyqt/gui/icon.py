# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtGui


class Icon(QtGui.QIcon):

    def __init__(self, icon=None):
        if isinstance(icon, pathlib.Path):
            icon = str(icon)
        super().__init__(icon)


if __name__ == "__main__":
    icon = Icon()
