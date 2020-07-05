# -*- coding: utf-8 -*-
"""
"""

import pathlib

from qtpy import QtCore


class Url(QtCore.QUrl):

    # def __str__(self):
    #     return self.absolutePath()

    def to_path(self) -> pathlib.Path:
        """get pathlib object from the URL

        Returns:
            Path
        """
        return pathlib.Path(self.path())

    def is_local_file(self) -> bool:
        return self.isLocalFile()
