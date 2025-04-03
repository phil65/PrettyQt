from __future__ import annotations

from typing import Literal, Self

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


StringFormatStr = Literal["with_braces", "without_braces", "id_128"]

STRING_FORMATS: bidict[StringFormatStr, QtCore.QUuid.StringFormat] = bidict(
    with_braces=QtCore.QUuid.StringFormat.WithBraces,
    without_braces=QtCore.QUuid.StringFormat.WithoutBraces,
    id_128=QtCore.QUuid.StringFormat.Id128,
)

VariantStr = Literal["unknown", "ncs", "dce", "microsoft", "reserved"]

VARIANTS: bidict[VariantStr, QtCore.QUuid.Variant] = bidict(
    unknown=QtCore.QUuid.Variant.VarUnknown,
    ncs=QtCore.QUuid.Variant.NCS,
    dce=QtCore.QUuid.Variant.DCE,
    microsoft=QtCore.QUuid.Variant.Microsoft,
    reserved=QtCore.QUuid.Variant.Reserved,
)

VersionStr = Literal["unknown", "time", "embedded_posix", "name", "random", "sha1"]

VERSION: bidict[VersionStr, QtCore.QUuid.Version] = bidict(
    unknown=QtCore.QUuid.Version.VerUnknown,
    time=QtCore.QUuid.Version.Time,
    embedded_posix=QtCore.QUuid.Version.EmbeddedPOSIX,
    name=QtCore.QUuid.Version.Name,
    # md5=QtCore.QUuid.Version.Md5,
    random=QtCore.QUuid.Version.Random,
    sha1=QtCore.QUuid.Version.Sha1,
)


class UuidMixin:
    def __repr__(self):
        return get_repr(self, self.toString())

    def __str__(self):
        return self.toString()

    def __bool__(self):
        return not self.isNull()

    def __reduce__(self):
        return type(self), (self.toString(),)

    def __format__(self, format_spec: StringFormatStr):
        return self.to_string(format_spec)

    def get_variant(self) -> VariantStr:
        return VARIANTS.inverse[self.variant()]

    def get_version(self) -> VersionStr:
        return VERSION.inverse[self.version()]

    @classmethod
    def create_uuid(cls) -> Self:
        # workaround for PySide2, not able to clone in ctor
        return cls(cls.createUuid().toString())

    def to_string(
        self, fmt: StringFormatStr | QtCore.QUuid.StringFormat = "with_braces"
    ) -> str:
        """Return string representation of the Uuid.

        Allowed values are "with_braces", "without_braces", "id_128"

        Args:
            fmt: Uuid format to use
        """
        return self.toString(STRING_FORMATS.get_enum_value(fmt))


class Uuid(UuidMixin, QtCore.QUuid):
    """Stores a Universally Unique Identifier (UUID)."""


if __name__ == "__main__":
    address = Uuid.create_uuid()
    print(repr(address))
