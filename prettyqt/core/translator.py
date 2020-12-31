import pathlib
from typing import Optional, Union

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QTranslator.__bases__ = (core.Object,)


class Translator(QtCore.QTranslator):
    def __bool__(self):
        return not self.isEmpty()

    def get_file_path(self) -> Optional[pathlib.Path]:
        path = self.filePath()
        if not path:
            return None
        return pathlib.Path(path)

    def load_file(self, path: Union[str, pathlib.Path]) -> bool:
        return self.load(str(path))
