from __future__ import annotations

from typing import Literal

from typing_extensions import Self

from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, get_repr


STRING_FORMATS = bidict(
    with_braces=QtCore.QUuid.StringFormat.WithBraces,
    without_braces=QtCore.QUuid.StringFormat.WithoutBraces,
    id_128=QtCore.QUuid.StringFormat.Id128,
)

StringFormatStr = Literal["with_braces", "without_braces", "id_128"]

VARIANTS = bidict(
    unknown=QtCore.QUuid.Variant.VarUnknown,
    ncs=QtCore.QUuid.Variant.NCS,
    dce=QtCore.QUuid.Variant.DCE,
    microsoft=QtCore.QUuid.Variant.Microsoft,
    reserved=QtCore.QUuid.Variant.Reserved,
)

VariantStr = Literal["unknown", "ncs", "dce", "microsoft", "reserved"]

VERSION = bidict(
    unknown=QtCore.QUuid.Version.VerUnknown,
    time=QtCore.QUuid.Version.Time,
    embedded_posix=QtCore.QUuid.Version.EmbeddedPOSIX,
    name=QtCore.QUuid.Version.Name,
    # md5=QtCore.QUuid.Version.Md5,
    random=QtCore.QUuid.Version.Random,
    sha1=QtCore.QUuid.Version.Sha1,
)

VersionStr = Literal["unknown", "time", "embedded_posix", "name", "random", "sha1"]


class UuidMixin:
    def __repr__(self):
        return get_repr(self, self.toString())

    def __str__(self):
        return self.toString()

    def __bool__(self):
        return not self.isNull()

    def __reduce__(self):
        return type(self), (self.toString(),)

    def get_variant(self) -> VariantStr:
        return VARIANTS.inverse[self.variant()]

    def get_version(self) -> VersionStr:
        return VERSION.inverse[self.version()]

    @classmethod
    def create_uuid(cls) -> Self:
        # workaround for PySide2, not able to clone in ctor
        return cls(cls.createUuid().toString())

    def to_string(self, fmt: StringFormatStr = "with_braces") -> str:
        """Return string representation of the Uuid.

        Allowed values are "with_braces", "without_braces", "id_128"

        Args:
            fmt: Uuid format to use

        Raises:
            InvalidParamError: Uuid format does not exist
        """
        if fmt not in STRING_FORMATS:
            raise InvalidParamError(fmt, STRING_FORMATS)
        return self.toString(STRING_FORMATS[fmt])


class Uuid(UuidMixin, QtCore.QUuid):
    pass


if __name__ == "__main__":
    address = Uuid.create_uuid()
    print(repr(address))
