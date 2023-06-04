from __future__ import annotations

import sys

from typing_extensions import Self

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class VersionNumber(QtCore.QVersionNumber):
    def __init__(self, *args, **kwargs):
        match args:
            case (str(),):
                args = [int(i) for i in args[0].split(".")][:3]
            case (tuple(),):
                args = args[0]
            # PySide6 Workaround:
            case (QtCore.QVersionNumber(),):
                args = (
                    args[0].majorVersion(),
                    args[0].minorVersion(),
                    args[0].microVersion(),
                )
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return get_repr(self, self.major(), self.minor(), self.micro())

    @property
    def _majorVersion(self) -> int:
        return self.majorVersion()

    @property
    def _minorVersion(self) -> int:
        return self.minorVersion()

    @property
    def _macroVersion(self) -> int:
        return self.macroVersion()

    __match_args__ = ("_majorVersion", "_minorVersion", "_macroVersion")

    def __reduce__(self):
        return type(self), (self.major(), self.minor(), self.micro())

    def __str__(self):
        return self.toString()

    def __eq__(self, other):
        if isinstance(other, str | tuple):
            other = VersionNumber(other)
        return super().__eq__(other)

    def __hash__(self):
        return hash((self.major(), self.minor(), self.micro()))

    def __gt__(self, other: datatypes.SemanticVersionType):
        if isinstance(other, str | tuple):
            other = VersionNumber(other)
        return super().__gt__(other)

    def __ge__(self, other: datatypes.SemanticVersionType):
        if isinstance(other, str | tuple):
            other = VersionNumber(other)
        return super().__ge__(other)

    def __lt__(self, other: datatypes.SemanticVersionType):
        if isinstance(other, str | tuple):
            other = VersionNumber(other)
        return super().__lt__(other)

    def __le__(self, other: datatypes.SemanticVersionType):
        if isinstance(other, str | tuple):
            other = VersionNumber(other)
        return super().__le__(other)

    @classmethod
    def from_string(cls, version_string: str) -> Self:
        return cls(cls.fromString(version_string))

    @classmethod
    def get_qt_version(cls) -> Self:
        return cls(*[int(i) for i in QtCore.__version__.split(".")])

    @classmethod
    def get_python_version(cls) -> Self:
        return cls(*sys.version_info[:3])

    def major(self) -> int:
        """An integer representing the major version."""
        return self.majorVersion()

    def minor(self) -> int:
        """An integer representing the minor version."""
        return self.minorVersion()

    def micro(self) -> int:
        """An integer representing the micro version."""
        return self.microVersion()


if __name__ == "__main__":
    version = VersionNumber(3, 0, 0)
