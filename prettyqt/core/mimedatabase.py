from __future__ import annotations

import os
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
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
        path: str | os.PathLike | QtCore.QFileInfo,
        match_mode: MatchModeStr = "default",
    ) -> core.MimeType:
        if match_mode not in MATCH_MODE:
            raise InvalidParamError(match_mode, MATCH_MODE)
        if isinstance(path, os.PathLike):
            path = os.fspath(path)
        mime_type = self.mimeTypeForFile(path, MATCH_MODE[match_mode])
        return core.MimeType(mime_type)
