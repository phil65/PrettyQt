# -*- coding: utf-8 -*-

from typing import Optional
import pathlib

from qtpy import QtCore

from prettyqt import core


QtCore.QTranslator.__bases__ = (core.Object,)


class Translator(QtCore.QTranslator):
    def get_file_path(self) -> Optional[pathlib.Path]:
        path = self.filePath()
        if not path:
            return None
        return pathlib.Path(path)
