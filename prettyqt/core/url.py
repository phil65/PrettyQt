from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Any, Literal, Self

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr, serializemixin


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


ComponentFormattingStr = Literal[
    "pretty_decoded",
    "encode_spaces",
    "encode_unicode",
    "encode_delimiters",
    "encode_reserved",
    "decode_reserved",
    "fully_encoded",
    "fully_decoded",
]

COMPONENT_FORMATTING_OPTIONS: bidict[
    ComponentFormattingStr, QtCore.QUrl.ComponentFormattingOption
] = bidict(
    pretty_decoded=QtCore.QUrl.ComponentFormattingOption.PrettyDecoded,
    encode_spaces=QtCore.QUrl.ComponentFormattingOption.EncodeSpaces,
    encode_unicode=QtCore.QUrl.ComponentFormattingOption.EncodeUnicode,
    encode_delimiters=QtCore.QUrl.ComponentFormattingOption.EncodeDelimiters,
    encode_reserved=QtCore.QUrl.ComponentFormattingOption.EncodeReserved,
    decode_reserved=QtCore.QUrl.ComponentFormattingOption.DecodeReserved,
    fully_encoded=QtCore.QUrl.ComponentFormattingOption.FullyEncoded,
    fully_decoded=QtCore.QUrl.ComponentFormattingOption.FullyDecoded,
)

ParsingModeStr = Literal["tolerant", "strict", "decoded"]

PARSING_MODES: bidict[FormattingOptionStr, QtCore.QUrl.ParsingMode] = bidict(
    tolerant=QtCore.QUrl.ParsingMode.TolerantMode,
    strict=QtCore.QUrl.ParsingMode.StrictMode,
    decoded=QtCore.QUrl.ParsingMode.DecodedMode,
)

FormattingOptionStr = Literal[
    "none",
    "remove_scheme",
    "remove_password",
    "remove_user_info",
    "remove_port",
    "remove_authority",
    "remove_path",
    "remove_query",
    "remove_fragment",
    "remove_filename",
    "prefer_local_file",
    "strip_trailing_slash",
    "normalize_path_segments",
]

FORMATTING_OPTIONS: bidict[FormattingOptionStr, QtCore.QUrl.UrlFormattingOption] = bidict(
    none=0,  # QtCore.QUrl.UrlFormattingOption.None
    remove_scheme=QtCore.QUrl.UrlFormattingOption.RemoveScheme,
    remove_password=QtCore.QUrl.UrlFormattingOption.RemovePassword,
    remove_user_info=QtCore.QUrl.UrlFormattingOption.RemoveUserInfo,
    remove_port=QtCore.QUrl.UrlFormattingOption.RemovePort,
    remove_authority=QtCore.QUrl.UrlFormattingOption.RemoveAuthority,
    remove_path=QtCore.QUrl.UrlFormattingOption.RemovePath,
    remove_query=QtCore.QUrl.UrlFormattingOption.RemoveQuery,
    remove_fragment=QtCore.QUrl.UrlFormattingOption.RemoveFragment,
    remove_filename=QtCore.QUrl.UrlFormattingOption.RemoveFilename,
    prefer_local_file=QtCore.QUrl.UrlFormattingOption.PreferLocalFile,
    strip_trailing_slash=QtCore.QUrl.UrlFormattingOption.StripTrailingSlash,
    normalize_path_segments=QtCore.QUrl.UrlFormattingOption.NormalizePathSegments,
)


class Url(serializemixin.SerializeMixin, QtCore.QUrl):
    """Convenient interface for working with URLs."""

    def __init__(self, *args, **kwargs):
        match args:
            case (os.PathLike(), *rest):
                path = os.fspath(args[0])
                if pathlib.Path(path).exists():
                    path = self.fromLocalFile(path)
                super().__init__(path, *rest, **kwargs)
            case _:
                super().__init__(*args, **kwargs)

    @property
    def _toString(self) -> str:
        return self.toString()

    __match_args__ = ("_toString",)

    # def __str__(self):
    #     return self.absolutePath()

    def __repr__(self):
        return get_repr(self, self.toString())

    def __str__(self):
        return self.toString()

    def __vfspath__(self) -> str:
        return self.toString()

    def serialize_fields(self):
        return dict(path=self.toString())

    def serialize(self) -> dict[str, Any]:
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
    def from_user_input(cls, url: str, working_dir: str | None = None) -> Self:
        if working_dir is None:
            working_dir = ""
        return cls(cls.fromUserInput(url, working_dir))

    @classmethod
    def from_local_file(cls, path: datatypes.PathType) -> Self:
        url = cls.fromLocalFile(os.fspath(path))
        return cls(url)

    def _has_explicit_scheme(self) -> bool:
        """Check if a url has an explicit scheme given."""
        return bool(
            self.isValid()
            and self.scheme()
            and (self.host() or self.path())
            and not self.path().startswith(":")
        )

    def is_special_url(self) -> bool:
        """Return True if url is an about:... or other special URL."""
        return self.scheme() in ("about", "file") if self.isValid() else False


if __name__ == "__main__":
    url = Url()
    str(url)
