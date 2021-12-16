from __future__ import annotations

import hashlib
import logging
import pathlib
from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, types


logger = logging.getLogger(__name__)

SYSTEM_FONT = bidict(
    general=QtGui.QFontDatabase.SystemFont.GeneralFont,
    fixed=QtGui.QFontDatabase.SystemFont.FixedFont,
    title=QtGui.QFontDatabase.SystemFont.TitleFont,
    smallest_readable=QtGui.QFontDatabase.SystemFont.SmallestReadableFont,
)

SystemFontStr = Literal["general", "fixed", "title", "smallest_readable"]

WRITING_SYSTEM = bidict(
    any=QtGui.QFontDatabase.WritingSystem.Any,
    latin=QtGui.QFontDatabase.WritingSystem.Latin,
    greek=QtGui.QFontDatabase.WritingSystem.Greek,
    cyrillic=QtGui.QFontDatabase.WritingSystem.Cyrillic,
    armenian=QtGui.QFontDatabase.WritingSystem.Armenian,
    hebrew=QtGui.QFontDatabase.WritingSystem.Hebrew,
    arabic=QtGui.QFontDatabase.WritingSystem.Arabic,
    syriac=QtGui.QFontDatabase.WritingSystem.Syriac,
    thaana=QtGui.QFontDatabase.WritingSystem.Thaana,
    devanagari=QtGui.QFontDatabase.WritingSystem.Devanagari,
    bengali=QtGui.QFontDatabase.WritingSystem.Bengali,
    gurmukhi=QtGui.QFontDatabase.WritingSystem.Gurmukhi,
    gujarati=QtGui.QFontDatabase.WritingSystem.Gujarati,
    oriya=QtGui.QFontDatabase.WritingSystem.Oriya,
    tamil=QtGui.QFontDatabase.WritingSystem.Tamil,
    telugu=QtGui.QFontDatabase.WritingSystem.Telugu,
    kannada=QtGui.QFontDatabase.WritingSystem.Kannada,
    malayalam=QtGui.QFontDatabase.WritingSystem.Malayalam,
    sinhala=QtGui.QFontDatabase.WritingSystem.Sinhala,
    thai=QtGui.QFontDatabase.WritingSystem.Thai,
    lao=QtGui.QFontDatabase.WritingSystem.Lao,
    tibetan=QtGui.QFontDatabase.WritingSystem.Tibetan,
    myanmar=QtGui.QFontDatabase.WritingSystem.Myanmar,
    georgian=QtGui.QFontDatabase.WritingSystem.Georgian,
    khmer=QtGui.QFontDatabase.WritingSystem.Khmer,
    simplified_chinese=QtGui.QFontDatabase.WritingSystem.SimplifiedChinese,
    traditional_chinese=QtGui.QFontDatabase.WritingSystem.TraditionalChinese,
    japanese=QtGui.QFontDatabase.WritingSystem.Japanese,
    korean=QtGui.QFontDatabase.WritingSystem.Korean,
    vietnamese=QtGui.QFontDatabase.WritingSystem.Vietnamese,
    symbol=QtGui.QFontDatabase.WritingSystem.Symbol,
    ogham=QtGui.QFontDatabase.WritingSystem.Ogham,
    runic=QtGui.QFontDatabase.WritingSystem.Runic,
    nko=QtGui.QFontDatabase.WritingSystem.Nko,
)

WritingSystemStr = Literal[
    "any",
    "latin",
    "greek",
    "cyrillic",
    "armenian",
    "hebrew",
    "arabic",
    "syriac",
    "thaana",
    "devanagari",
    "bengali",
    "gurmukhi",
    "gujarati",
    "oriya",
    "tamil",
    "telugu",
    "kannada",
    "malayalam",
    "sinhala",
    "thai",
    "lao",
    "tibetan",
    "myanmar",
    "georgian",
    "khmer",
    "simplified_chinese",
    "traditional_chinese",
    "japanese",
    "korean",
    "vietnamese",
    "symbol",
    "ogham",
    "runic",
    "nko",
]


class FontDatabase(QtGui.QFontDatabase):
    font_paths: dict[str, int] = dict()

    @classmethod
    def add_fonts_from_folder(cls, path: types.PathType):
        path = pathlib.Path(path)
        for p in path.iterdir():
            if p.suffix.lower() in [".ttf", ".otf"]:
                logger.debug(f"adding font {p!r} to database.")
                cls.addApplicationFont(str(p))

    @classmethod
    def add_font(cls, path: types.PathType, ttf_hash: str | None = None) -> int:
        path = pathlib.Path(path)
        font_id = cls.addApplicationFont(str(path))
        if not cls.applicationFontFamilies(font_id):
            raise RuntimeError(
                f"Font {path!r} appears to be empty. "
                "If you are on Windows 10, please read "
                "https://support.microsoft.com/"
                "en-us/kb/3053676"
            )
        if ttf_hash is not None:
            content = path.read_bytes()
            if hashlib.md5(content).hexdigest() != ttf_hash:
                raise OSError(f"Font is corrupt at: {path!r}")
        cls.font_paths[str(path)] = font_id
        return font_id

    @classmethod
    def remove_font(cls, font: types.PathType | int):
        font_id = font if isinstance(font, int) else cls.font_paths[str(font)]
        cls.removeApplicationFont(font_id)

    @classmethod
    def get_system_font(cls, font_type: SystemFontStr):
        if font_type not in SYSTEM_FONT:
            raise InvalidParamError(font_type, SYSTEM_FONT)
        return cls.systemFont(SYSTEM_FONT[font_type])


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    db = FontDatabase()
    print(db.families())
