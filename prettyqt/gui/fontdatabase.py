from __future__ import annotations

import hashlib
import logging
import os
import pathlib
from typing import Literal, Optional, Union

from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


logger = logging.getLogger(__name__)

SYSTEM_FONT = bidict(
    general=QtGui.QFontDatabase.GeneralFont,
    fixed=QtGui.QFontDatabase.FixedFont,
    title=QtGui.QFontDatabase.TitleFont,
    smallest_readable=QtGui.QFontDatabase.SmallestReadableFont,
)

SystemFontStr = Literal["general", "fixed", "title", "smallest_readable"]

WRITING_SYSTEM = bidict(
    any=QtGui.QFontDatabase.Any,
    latin=QtGui.QFontDatabase.Latin,
    greek=QtGui.QFontDatabase.Greek,
    cyrillic=QtGui.QFontDatabase.Cyrillic,
    armenian=QtGui.QFontDatabase.Armenian,
    hebrew=QtGui.QFontDatabase.Hebrew,
    arabic=QtGui.QFontDatabase.Arabic,
    syriac=QtGui.QFontDatabase.Syriac,
    thaana=QtGui.QFontDatabase.Thaana,
    devanagari=QtGui.QFontDatabase.Devanagari,
    bengali=QtGui.QFontDatabase.Bengali,
    gurmukhi=QtGui.QFontDatabase.Gurmukhi,
    gujarati=QtGui.QFontDatabase.Gujarati,
    oriya=QtGui.QFontDatabase.Oriya,
    tamil=QtGui.QFontDatabase.Tamil,
    telugu=QtGui.QFontDatabase.Telugu,
    kannada=QtGui.QFontDatabase.Kannada,
    malayalam=QtGui.QFontDatabase.Malayalam,
    sinhala=QtGui.QFontDatabase.Sinhala,
    thai=QtGui.QFontDatabase.Thai,
    lao=QtGui.QFontDatabase.Lao,
    tibetan=QtGui.QFontDatabase.Tibetan,
    myanmar=QtGui.QFontDatabase.Myanmar,
    georgian=QtGui.QFontDatabase.Georgian,
    khmer=QtGui.QFontDatabase.Khmer,
    simplified_chinese=QtGui.QFontDatabase.SimplifiedChinese,
    traditional_chinese=QtGui.QFontDatabase.TraditionalChinese,
    japanese=QtGui.QFontDatabase.Japanese,
    korean=QtGui.QFontDatabase.Korean,
    vietnamese=QtGui.QFontDatabase.Vietnamese,
    symbol=QtGui.QFontDatabase.Symbol,
    ogham=QtGui.QFontDatabase.Ogham,
    runic=QtGui.QFontDatabase.Runic,
    nko=QtGui.QFontDatabase.Nko,
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
    @classmethod
    def add_fonts_from_folder(cls, path: Union[str, os.PathLike]):
        path = pathlib.Path(path)
        for p in path.iterdir():
            if p.suffix.lower() in [".ttf", ".otf"]:
                logger.debug(f"adding font {p} to database.")
                cls.addApplicationFont(str(p))

    @classmethod
    def add_font(
        cls, path: Union[str, os.PathLike], ttf_hash: Optional[str] = None
    ) -> int:
        path = pathlib.Path(path)
        font_id = cls.addApplicationFont(str(path))
        if not cls.applicationFontFamilies(font_id):
            raise RuntimeError(
                f"Font '{path}' appears to be empty. "
                "If you are on Windows 10, please read "
                "https://support.microsoft.com/"
                "en-us/kb/3053676 "
                "to know how to prevent Windows from blocking "
                "the fonts that come with QtAwesome."
            )
        if ttf_hash is not None:
            content = path.read_bytes()
            if hashlib.md5(content).hexdigest() != ttf_hash:
                raise OSError(f"Font is corrupt at: '{path}'")
        return font_id

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
