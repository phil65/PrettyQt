from __future__ import annotations

import os
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, datatypes


MATCH_MODE = bidict(
    default=QtCore.QMimeDatabase.MatchMode.MatchDefault,
    extension=QtCore.QMimeDatabase.MatchMode.MatchExtension,
    content=QtCore.QMimeDatabase.MatchMode.MatchContent,
)

MatchModeStr = Literal["default", "extension", "content"]


class MimeDatabase(QtCore.QMimeDatabase):
    def get_mime_type_for_file(
        self,
        path: datatypes.PathType | QtCore.QFileInfo,
        match_mode: MatchModeStr = "default",
    ) -> core.MimeType:
        if match_mode not in MATCH_MODE:
            raise InvalidParamError(match_mode, MATCH_MODE)
        if isinstance(path, os.PathLike):
            path = os.fspath(path)
        mime_type = self.mimeTypeForFile(path, MATCH_MODE[match_mode])
        return core.MimeType(mime_type)

    def get_mime_type_for_data(
        self, data: datatypes.ByteArrayType | QtCore.QIODevice
    ) -> core.MimeType:
        return core.MimeType(self.mimeTypeForData(data))

    def get_mime_type_for_filename_and_data(
        self, filename: os.PathLike, data: datatypes.ByteArrayType | QtCore.QIODevice
    ) -> core.MimeType:
        path = os.fspath(filename)
        return core.MimeType(self.mimeTypeForFileNameAndData(path, data))

    def get_mime_type_for_name(self, name: str) -> core.MimeType:
        return core.MimeType(self.mimeTypeForName(name))

    def get_mime_type_for_url(self, url: QtCore.QUrl | str) -> core.MimeType:
        url = QtCore.QUrl(url) if isinstance(url, str) else url
        return core.MimeType(self.mimeTypeForUrl(url))

    def get_mime_types_for_filename(
        self, filename: datatypes.PathType
    ) -> list[core.MimeType]:
        path = os.fspath(filename)
        return [core.MimeType(i) for i in self.mimeTypesForFileName(path)]


if __name__ == "__main__":
    db = MimeDatabase()
    print(db.get_mime_type_for_file("C:/test.log"))
