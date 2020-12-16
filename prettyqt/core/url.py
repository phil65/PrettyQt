from __future__ import annotations

import pathlib
from typing import Optional, Union

from qtpy import QtCore

from prettyqt.utils import bidict


COMPONENT_FORMATTING_OPTIONS = bidict(
    pretty_decoded=QtCore.QUrl.PrettyDecoded,
    encode_spaces=QtCore.QUrl.EncodeSpaces,
    encode_unicode=QtCore.QUrl.EncodeUnicode,
    encode_delimiters=QtCore.QUrl.EncodeDelimiters,
    encode_reserved=QtCore.QUrl.EncodeReserved,
    decode_reserved=QtCore.QUrl.DecodeReserved,
    fully_encoded=QtCore.QUrl.FullyEncoded,
    fully_decoded=QtCore.QUrl.FullyDecoded,
)


PARSING_MODES = bidict(
    tolerant=QtCore.QUrl.TolerantMode,
    strict=QtCore.QUrl.StrictMode,
    decoded=QtCore.QUrl.DecodedMode,
)

FORMATTING_OPTIONS = bidict(
    none=0,  # QtCore.QUrl.None
    remove_scheme=QtCore.QUrl.RemoveScheme,
    remove_password=QtCore.QUrl.RemovePassword,
    remove_user_info=QtCore.QUrl.RemoveUserInfo,
    remove_port=QtCore.QUrl.RemovePort,
    remove_authority=QtCore.QUrl.RemoveAuthority,
    remove_path=QtCore.QUrl.RemovePath,
    remove_query=QtCore.QUrl.RemoveQuery,
    remove_fragment=QtCore.QUrl.RemoveFragment,
    remove_filename=QtCore.QUrl.RemoveFilename,
    prefer_local_file=QtCore.QUrl.PreferLocalFile,
    strip_trailing_slash=QtCore.QUrl.StripTrailingSlash,
    normalize_path_segments=QtCore.QUrl.NormalizePathSegments,
)


class Url(QtCore.QUrl):
    def __init__(self, path: Optional[Union[QtCore.QUrl, str, pathlib.Path]] = None):
        if path is None:
            super().__init__()
        else:
            super().__init__(str(path) if not isinstance(path, QtCore.QUrl) else path)
            if isinstance(path, pathlib.Path):
                self.setScheme("file")

    # def __str__(self):
    #     return self.absolutePath()

    def __repr__(self):
        return f"{type(self).__name__}({self.toString()!r})"

    def __str__(self):
        return self.toString()

    def serialize_fields(self):
        return dict(path=self.toString())

    def serialize(self):
        return self.serialize_fields()

    def to_string(self) -> str:
        return self.toString()

    def to_path(self) -> pathlib.Path:
        """Get pathlib object from the URL.

        Returns:
            Path
        """
        return pathlib.Path(str(self))

    def is_local_file(self) -> bool:
        return self.isLocalFile()

    @classmethod
    def from_user_input(cls, url: str, working_dir: Optional[str] = None) -> Url:
        if working_dir is None:
            working_dir = ""
        return cls(cls.fromUserInput(url, working_dir))


if __name__ == "__main__":
    url = Url()
    str(url)
