from __future__ import annotations

import os
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, types


MATCH_MODE = bidict(
    default=QtCore.QMimeDatabase.MatchMode.MatchDefault,
    extension=QtCore.QMimeDatabase.MatchMode.MatchExtension,
    content=QtCore.QMimeDatabase.MatchMode.MatchContent,
)

MatchModeStr = Literal["default", "extension", "content"]


class MimeDatabase(QtCore.QMimeDatabase):
    def get_mime_type_for_file(
        self,
        path: types.PathType | QtCore.QFileInfo,
        match_mode: MatchModeStr = "default",
    ) -> core.MimeType:
        if match_mode not in MATCH_MODE:
            raise InvalidParamError(match_mode, MATCH_MODE)
        if isinstance(path, os.PathLike):
            path = os.fspath(path)
        mime_type = self.mimeTypeForFile(path, MATCH_MODE[match_mode])
        return core.MimeType(mime_type)
