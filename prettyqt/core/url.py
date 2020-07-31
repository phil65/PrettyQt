# -*- coding: utf-8 -*-

from typing import Union

import pathlib

from qtpy import QtCore


class Url(QtCore.QUrl):
    def __init__(self, path: Union[QtCore.QUrl, str, pathlib.Path]):

        super().__init__(str(path) if not isinstance(path, QtCore.QUrl) else path)
        if isinstance(path, pathlib.Path):
            self.setScheme("file")

    # def __str__(self):
    #     return self.absolutePath()

    def __repr__(self):
        return f"core.Url('{self.toString(self.PreferLocalFile)}')"

    def __str__(self):
        return self.toString(self.PreferLocalFile)

    def to_path(self) -> pathlib.Path:
        """Get pathlib object from the URL.

        Returns:
            Path
        """
        return pathlib.Path(str(self))

    def is_local_file(self) -> bool:
        return self.isLocalFile()
