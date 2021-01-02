from __future__ import annotations

import os
import pathlib
from typing import Optional, Set, Union

from prettyqt import core
from prettyqt.qt import QtCore


LOCALIZATION_PATH = pathlib.Path(__file__).parent.parent / "localization"


QtCore.QTranslator.__bases__ = (core.Object,)


class Translator(QtCore.QTranslator):
    def __bool__(self):
        return not self.isEmpty()

    def get_file_path(self) -> Optional[pathlib.Path]:
        path = self.filePath()
        if not path:
            return None
        return pathlib.Path(path)

    def load_file(self, path: Union[str, os.PathLike]):
        path = pathlib.Path(path)
        if not self.load(path.name, str(path.parent)):
            raise OSError(f"Invalid language file {path}")

    @classmethod
    def get_available_languages(cls) -> Set[str]:
        return {
            str(path).split("_", maxsplit=1)[1][:-3]
            for path in LOCALIZATION_PATH.iterdir()
        }

    @classmethod
    def for_language(cls, language: str) -> Translator:
        # if language not in cls.get_available_languages():
        #     raise ValueError("Language does not exist")
        file = LOCALIZATION_PATH / f"language_{language}.qm"
        translator = cls()
        translator.load_file(file)
        return translator


if __name__ == "__main__":
    print(Translator.get_available_languages())
    app = core.app()
    translator = Translator.for_language("de")
