from __future__ import annotations

import os
from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict, datatypes


MatchModeStr = Literal["default", "extension", "content"]

MATCH_MODE: bidict[MatchModeStr, core.QMimeDatabase.MatchMode] = bidict(
    default=core.QMimeDatabase.MatchMode.MatchDefault,
    extension=core.QMimeDatabase.MatchMode.MatchExtension,
    content=core.QMimeDatabase.MatchMode.MatchContent,
)


class MimeDatabase(core.QMimeDatabase):
    """Maintains a database of MIME types."""

    def get_mime_type_for_file(
        self,
        path: datatypes.PathType | core.QFileInfo,
        match_mode: MatchModeStr | core.QMimeDatabase.MatchMode = "default",
    ) -> core.MimeType:
        if isinstance(path, os.PathLike):
            path = os.fspath(path)
        mime_type = self.mimeTypeForFile(path, MATCH_MODE.get_enum_value(match_mode))
        return core.MimeType(mime_type)

    def get_mime_type_for_data(
        self, data: datatypes.ByteArrayType | core.QIODevice
    ) -> core.MimeType:
        return core.MimeType(self.mimeTypeForData(data))

    def get_mime_type_for_filename_and_data(
        self,
        filename: str | os.PathLike[str],
        data: datatypes.ByteArrayType | core.QIODevice,
    ) -> core.MimeType:
        path = os.fspath(filename)
        return core.MimeType(self.mimeTypeForFileNameAndData(path, data))

    def get_mime_type_for_name(self, name: str) -> core.MimeType:
        return core.MimeType(self.mimeTypeForName(name))

    def get_mime_type_for_url(self, url: core.QUrl | str) -> core.MimeType:
        url = core.QUrl(url) if isinstance(url, str) else url
        return core.MimeType(self.mimeTypeForUrl(url))

    def get_mime_types_for_filename(
        self, filename: datatypes.PathType
    ) -> list[core.MimeType]:
        path = os.fspath(filename)
        return [core.MimeType(i) for i in self.mimeTypesForFileName(path)]


if __name__ == "__main__":
    db = MimeDatabase()
    print(db.get_mime_type_for_file("C:/test.log"))
