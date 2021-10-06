from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


OS_TYPE = bidict(
    android=QtCore.QOperatingSystemVersion.OSType.Android,
    ios=QtCore.QOperatingSystemVersion.OSType.IOS,
    mac_os=QtCore.QOperatingSystemVersion.OSType.MacOS,
    tv_os=QtCore.QOperatingSystemVersion.OSType.TvOS,
    watch_os=QtCore.QOperatingSystemVersion.OSType.WatchOS,
    windows=QtCore.QOperatingSystemVersion.OSType.Windows,
    unknown=QtCore.QOperatingSystemVersion.OSType.Unknown,
)

OsTypeStr = Literal["android", "ios", "mac_os", "tv_os", "watch_os", "windows", "unknown"]


class OperatingSystemVersion(QtCore.QOperatingSystemVersion):
    def __init__(
        self,
        typ: QtCore.QOperatingSystemVersion.OSType | str,
        major: int,
        minor: int | None = None,
        micro: int | None = None,
    ):
        if isinstance(typ, str):
            os_type = OS_TYPE[typ]
        else:
            os_type = typ
        if minor is None:
            minor = -1
        if micro is None:
            micro = -1
        super().__init__(os_type, major, minor, micro)

    def __repr__(self):
        return (
            f"{type(self).__name__}({self.get_type()!r}, {self.majorVersion()}, "
            f"{self.minorVersion()}, {self.microVersion()})"
        )

    def __reduce__(self):
        return (
            type(self),
            (
                self.get_type(),
                self.majorVersion(),
                self.minorVersion(),
                self.microVersion(),
            ),
        )

    def __eq__(self, other):
        if not isinstance(other, OperatingSystemVersion):
            return False
        return (
            self.get_type() == other.get_type()
            and self.get_versionnumber() == other.get_versionnumber()
        )

    def __hash__(self):
        return hash(
            (
                self.get_type(),
                self.majorVersion(),
                self.minorVersion(),
                self.microVersion(),
            )
        )

    def get_type(self) -> OsTypeStr:
        """Get current os type.

        Returns:
            current os type
        """
        return OS_TYPE.inverse[self.type()]

    def get_versionnumber(self) -> core.VersionNumber:
        return core.VersionNumber(
            self.majorVersion(), self.minorVersion(), self.microVersion()
        )


if __name__ == "__main__":
    version = OperatingSystemVersion("android", 11)
    print(repr(version))
