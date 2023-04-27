from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


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
        os_type = OS_TYPE[typ] if isinstance(typ, str) else typ
        if minor is None:
            minor = -1
        if micro is None:
            micro = -1
        super().__init__(os_type, major, minor, micro)

    def __repr__(self):
        return get_repr(
            self,
            self.get_type(),
            self.majorVersion(),
            self.minorVersion(),
            self.microVersion(),
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
        return (
            (
                self.type() == other.type()
                and self.majorVersion() == other.majorVersion()
                and self.minorVersion() == other.minorVersion()
                and self.microVersion() == other.microVersion()
            )
            if isinstance(other, QtCore.QOperatingSystemVersion)
            else False
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
