import pathlib
from typing import Optional

from qtpy import QtCore

from prettyqt import core


QtCore.QTranslator.__bases__ = (core.Object,)


class Translator(QtCore.QTranslator):
    def __bool__(self):
        return not self.isEmpty()

    def get_file_path(self) -> Optional[pathlib.Path]:
        path = self.filePath()
        if not path:
            return None
        return pathlib.Path(path)
