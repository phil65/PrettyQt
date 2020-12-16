from qtpy import QtCore

from prettyqt.utils import bidict


STRING_FORMATS = bidict(
    with_braces=QtCore.QUuid.WithBraces,
    without_braces=QtCore.QUuid.WithoutBraces,
    id_128=QtCore.QUuid.Id128,
)

VARIANTS = bidict(
    unknown=QtCore.QUuid.VarUnknown,
    ncs=QtCore.QUuid.NCS,
    dce=QtCore.QUuid.DCE,
    microsoft=QtCore.QUuid.Microsoft,
    reserved=QtCore.QUuid.Reserved,
)

VERSION = bidict(
    unknown=QtCore.QUuid.VerUnknown,
    time=QtCore.QUuid.Time,
    embedded_posix=QtCore.QUuid.EmbeddedPOSIX,
    name=QtCore.QUuid.Name,
    # md5=QtCore.QUuid.Md5,
    random=QtCore.QUuid.Random,
    sha1=QtCore.QUuid.Sha1,
)


class Uuid(QtCore.QUuid):
    def __repr__(self):
        return f"{self.__class__.__name__}({self.toString()!r})"

    def __str__(self):
        return self.toString()

    def __bool__(self):
        return not self.isNull()

    def __reduce__(self):
        return self.__class__, (self.toString(),)

    def get_variant(self) -> str:
        return VARIANTS.inverse[self.variant()]

    def get_version(self) -> str:
        return VERSION.inverse[self.version()]

    @classmethod
    def create_uuid(cls):
        # workaround for PySide2, not able to clone in ctor
        return cls(cls.createUuid().toString())


if __name__ == "__main__":
    address = Uuid.create_uuid()
    print(repr(address))
