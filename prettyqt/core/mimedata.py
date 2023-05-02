from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from typing_extensions import Self

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, helpers


class MimeData(core.ObjectMixin, QtCore.QMimeData):
    def __len__(self):
        return len(self.formats())

    # def __getitem__(self, index: str) -> str:
    #     return self.get_data(index)

    # def __setitem__(self, index: str, value: datatypes.ByteArrayType):
    #     if isinstance(value, str):
    #         value = value.encode()
    #     if not isinstance(value, QtCore.QByteArray):
    #         value = QtCore.QByteArray(value)
    #     self.setData(index, value)

    def __contains__(self, fmt: str):
        return self.hasFormat(fmt)

    def __delitem__(self, index: str):
        self.removeFormat(index)

    def set_data(self, mime_type: str, data: str):
        self.setData(mime_type, QtCore.QByteArray(data.encode()))

    def set_json_data(self, mime_type: str, data: datatypes.JSONType):
        self.setData(mime_type, QtCore.QByteArray(helpers.dump_json(data)))

    def get_data(self, mime_type: str) -> str:
        return bytes(self.data(mime_type)).decode()

    def get_json_data(self, mime_type: str) -> datatypes.JSONType:
        data = self.data(mime_type)
        return helpers.load_json(bytes(data))

    def keys(self) -> list[str]:
        return self.formats()

    def values(self) -> Iterator[Any]:
        return (self.get_data(key) for key in self.formats())

    def set_svg_data(self, string: str):
        data = string.encode()
        self.setData("image/svg+xml", data)

    def set_path_data(self, paths: list[datatypes.PathType]):
        urls = [core.Url.from_local_file(p) for p in paths]
        self.setUrls(urls)

    def set_urls(self, paths: list[datatypes.PathType]):
        urls = [core.Url(p) for p in paths]
        self.setUrls(urls)

    def get_urls(self) -> list[core.Url]:
        return [core.Url(url) for url in self.urls()]

    @classmethod
    def for_file(
        cls,
        path: datatypes.PathType | QtCore.QFileInfo,
        match_mode: core.mimedatabase.MatchModeStr = "default",
    ) -> MimeData:
        db = core.MimeDatabase()
        mime_type = db.get_mime_type_for_file(path, match_mode)
        return cls(mime_type)

    def to_dict(self) -> dict[str, bytes]:
        return {i: self.data(i).data() for i in self.formats()}

    @classmethod
    def clone(cls, other: QtCore.QMimeData) -> Self:
        mime = cls()
        for fmt in other.formats():
            mime.setData(fmt, other.data(fmt))
        return mime


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    c = app.get_clipboard()
    mime_data = c.mimeData()
    mime_data = MimeData.clone(mime_data)
    print(mime_data.to_dict())
