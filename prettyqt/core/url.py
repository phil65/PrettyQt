# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtCore


class Url(QtCore.QUrl):

    # def __str__(self):
    #     return self.absolutePath()

    def to_path(self) -> pathlib.Path:
        return pathlib.Path(self.path())

    def is_local_file(self) -> bool:
        return self.isLocalFile()
