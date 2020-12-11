from __future__ import annotations

import sys

from qtpy import QtCore
import qtpy


class VersionNumber(QtCore.QVersionNumber):
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], str):
                args = [int(i) for i in args[0].split(".")]
            elif isinstance(args[0], tuple):
                args = args[0]
        return super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"VersionNumber({self.major()}, {self.minor()}, {self.micro()})"

    def __reduce__(self):
        return (self.__class__, (self.major(), self.minor(), self.micro()))

    def __str__(self):
        return self.toString()

    def __eq__(self, other):
        if isinstance(other, (str, tuple)):
            other = VersionNumber(other)
        return super().__eq__(other)

    def __gt__(self, other):
        if isinstance(other, (str, tuple)):
            other = VersionNumber(other)
        return super().__gt__(other)

    def __ge__(self, other):
        if isinstance(other, (str, tuple)):
            other = VersionNumber(other)
        return super().__ge__(other)

    def __lt__(self, other):
        if isinstance(other, (str, tuple)):
            other = VersionNumber(other)
        return super().__lt__(other)

    def __le__(self, other):
        if isinstance(other, (str, tuple)):
            other = VersionNumber(other)
        return super().__le__(other)

    @classmethod
    def get_qt_version(cls) -> VersionNumber:
        return cls(*[int(i) for i in qtpy.QT_VERSION.split(".")])

    @classmethod
    def get_python_version(cls) -> VersionNumber:
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
