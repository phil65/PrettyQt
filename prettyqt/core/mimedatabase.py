import pathlib
from typing import Literal, Union

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


MATCH_MODE = bidict(
    default=QtCore.QMimeDatabase.MatchDefault,
    extension=QtCore.QMimeDatabase.MatchExtension,
    content=QtCore.QMimeDatabase.MatchContent,
)

MatchModeStr = Literal["default", "extension", "content"]


class MimeDatabase(QtCore.QMimeDatabase):
    def get_mime_type_for_file(
        self,
        path: Union[str, pathlib.Path, QtCore.QFileInfo],
        match_mode: MatchModeStr = "default",
    ) -> core.MimeType:
        if match_mode not in MATCH_MODE:
            raise InvalidParamError(match_mode, MATCH_MODE)
        if isinstance(path, pathlib.Path):
            path = str(path)
        mime_type = self.mimeTypeForFile(path, MATCH_MODE[match_mode])
        return core.MimeType(mime_type)
