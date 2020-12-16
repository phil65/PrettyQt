import logging
import pathlib
from typing import Literal, Union

from qtpy import QtGui

from prettyqt.utils import InvalidParamError, bidict


logger = logging.getLogger(__name__)

SYSTEM_FONT = bidict(
    general=QtGui.QFontDatabase.GeneralFont,
    fixed=QtGui.QFontDatabase.FixedFont,
    title=QtGui.QFontDatabase.TitleFont,
    smallest_readable=QtGui.QFontDatabase.SmallestReadableFont,
)

SystemFontStr = Literal["general", "fixed", "title", "smallest_readable"]


class FontDatabase(QtGui.QFontDatabase):
    @classmethod
    def add_fonts_from_folder(cls, path: Union[str, pathlib.Path]):
        if isinstance(path, str):
            path = pathlib.Path(path)
        for p in path.iterdir():
            if p.suffix.lower() in [".ttf", ".otf"]:
                logger.debug(f"adding font {p} to database.")
                cls.addApplicationFont(str(p))

    def get_system_font(self, font_type: SystemFontStr):
        if font_type not in SYSTEM_FONT:
            raise InvalidParamError(font_type, SYSTEM_FONT)
        return self.systemFont(SYSTEM_FONT[font_type])


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    db = FontDatabase()
    print(db.families())
