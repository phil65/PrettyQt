from typing import TYPE_CHECKING, Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


EncodingStr = Literal[
    "utf8",
    "utf16",
    "utf16_le",
    "utf16_be",
    "utf32",
    "utf32_le",
    "utf32_be",
    "latin1",
    "system",
]

ENCODING: bidict[EncodingStr, QtCore.QStringConverter.Encoding] = bidict(
    utf8=QtCore.QStringConverter.Encoding.Utf8,
    utf16=QtCore.QStringConverter.Encoding.Utf16,
    utf16_le=QtCore.QStringConverter.Encoding.Utf16LE,
    utf16_be=QtCore.QStringConverter.Encoding.Utf16BE,
    utf32=QtCore.QStringConverter.Encoding.Utf32,
    utf32_le=QtCore.QStringConverter.Encoding.Utf32LE,
    utf32_be=QtCore.QStringConverter.Encoding.Utf32BE,
    latin1=QtCore.QStringConverter.Encoding.Latin1,
    system=QtCore.QStringConverter.Encoding.System,
)

FlagStr = Literal[
    "stateless",
    "convert_invalid_to_null",
    "write_bom",
    "convert_initial_bom",
    "uses_icu",
]

FLAG: bidict[FlagStr, QtCore.QStringConverter.Flag] = bidict(
    stateless=QtCore.QStringConverter.Flag.Stateless,
    convert_invalid_to_null=QtCore.QStringConverter.Flag.ConvertInvalidToNull,
    write_bom=QtCore.QStringConverter.Flag.WriteBom,
    convert_initial_bom=QtCore.QStringConverter.Flag.ConvertInitialBom,
    uses_icu=QtCore.QStringConverter.Flag.UsesIcu,
)

FinalizeResultErrorStr = Literal["none", "invalid_characters", "not_enough_space"]

FINALIZE_RESULT_ERROR: bidict[
    FinalizeResultErrorStr, QtCore.QStringConverter.FinalizeResultError
] = bidict(
    none=QtCore.QStringConverter.FinalizeResultError.NoError,
    invalid_characters=QtCore.QStringConverter.FinalizeResultError.InvalidCharacters,
    not_enough_space=QtCore.QStringConverter.FinalizeResultError.NotEnoughSpace,
)


if TYPE_CHECKING:
    _StringConverterBase = QtCore.QStringConverter
else:
    _StringConverterBase = object


class StringConverterMixin(_StringConverterBase):
    def __repr__(self):
        return get_repr(self, self.get_name())

    def __bool__(self):
        return self.isValid()

    def get_name(self) -> str | None:
        name = self.name()
        if name is None:
            return None
        return name if isinstance(name, str) else bytes(name).decode()

    @staticmethod
    def get_name_for_encoding(
        encoding: EncodingStr | QtCore.QStringConverter.Encoding,
    ) -> str:
        name = QtCore.QStringConverter.nameForEncoding(ENCODING.get_enum_value(encoding))
        return name if isinstance(name, str) else bytes(name).decode()


class StringConverter(StringConverterMixin, QtCore.QStringConverter):
    """Base class for encoding and decoding text."""
