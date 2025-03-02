from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, Self

from prettyqt import core, paths


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class TranslatorMixin(core.ObjectMixin):
    def __bool__(self):
        return not self.isEmpty()

    def get_file_path(self) -> pathlib.Path | None:
        path = self.filePath()
        return pathlib.Path(path) if path else None

    def load_file(self, path: datatypes.PathType):
        path = pathlib.Path(path)
        if not self.load(path.name, str(path.parent)):
            msg = f"Invalid language file {path}"
            raise OSError(msg)

    @classmethod
    def get_available_languages(cls) -> set[str]:
        return {
            str(path).split("_", maxsplit=1)[1][:-3]
            for path in paths.LOCALIZATION_PATH.iterdir()
        }

    @classmethod
    def for_language(cls, language: str) -> Self:
        # if language not in cls.get_available_languages():
        #     raise ValueError("Language does not exist")
        file = paths.LOCALIZATION_PATH / f"language_{language}.qm"
        translator = cls()
        translator.load_file(file)
        return translator

    @classmethod
    def for_system_language(cls) -> Self:
        translator = cls()
        if not translator.load(
            f"qt_{core.Locale.system().name()}",
            str(core.LibraryInfo.get_location("translations")),
        ):
            msg = "Could not get translator for system language"
            raise OSError(msg)
        return translator


class Translator(TranslatorMixin, core.QTranslator):
    """Internationalization support for text output."""


if __name__ == "__main__":
    print(Translator.get_available_languages())
    app = core.app()
    translator = Translator.for_language("de")
