from __future__ import annotations

import pathlib

from prettyqt import core, paths
from prettyqt.qt import QtCore
from prettyqt.utils import types


QtCore.QTranslator.__bases__ = (core.Object,)


class Translator(QtCore.QTranslator):
    def __bool__(self):
        return not self.isEmpty()

    def get_file_path(self) -> pathlib.Path | None:
        path = self.filePath()
        if not path:
            return None
        return pathlib.Path(path)

    def load_file(self, path: types.PathType):
        path = pathlib.Path(path)
        if not self.load(path.name, str(path.parent)):
            raise OSError(f"Invalid language file {path}")

    @classmethod
    def get_available_languages(cls) -> set[str]:
        return {
            str(path).split("_", maxsplit=1)[1][:-3]
            for path in paths.LOCALIZATION_PATH.iterdir()
        }

    @classmethod
    def for_language(cls, language: str) -> Translator:
        # if language not in cls.get_available_languages():
        #     raise ValueError("Language does not exist")
        file = paths.LOCALIZATION_PATH / f"language_{language}.qm"
        translator = cls()
        translator.load_file(file)
        return translator

    @classmethod
    def for_system_language(cls) -> Translator:
        translator = cls()
        if not translator.load(
            "qt_" + core.Locale.system().name(),
            str(core.LibraryInfo.get_location("translations")),
        ):
            raise OSError("Could not get translator for system language")
        return translator


if __name__ == "__main__":
    print(Translator.get_available_languages())
    app = core.app()
    translator = Translator.for_language("de")
