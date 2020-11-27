# -*- coding: utf-8 -*-

from typing import Union, Optional

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict

OS_TYPE = bidict(
    android=QtCore.QOperatingSystemVersion.Android,
    ios=QtCore.QOperatingSystemVersion.IOS,
    mac_os=QtCore.QOperatingSystemVersion.MacOS,
    tv_os=QtCore.QOperatingSystemVersion.TvOS,
    watch_os=QtCore.QOperatingSystemVersion.WatchOS,
    windows=QtCore.QOperatingSystemVersion.Windows,
    unknown=QtCore.QOperatingSystemVersion.Unknown,
)


class OperatingSystemVersion(QtCore.QOperatingSystemVersion):
    def __init__(
        self,
        typ: Union[int, str],
        major: int,
        minor: Optional[int] = None,
        micro: Optional[int] = None,
    ):
        if isinstance(typ, str):
            typ = OS_TYPE[typ]
        if minor is None:
            minor = -1
        if micro is None:
            micro = -1
        super().__init__(typ, major, minor, micro)

    def get_type(self) -> str:
        """Get current os type.

        Possible values: "android", "ios", "mac_os", "tv_os", "watch_os", "windows",
                         "unknown"

        Returns:
            current os type
        """
        return OS_TYPE.inv[self.type()]

    def get_versionnumber(self) -> core.VersionNumber:
        return core.VersionNumber(
            self.majorVersion(), self.minorVersion(), self.microVersion()
        )


if __name__ == "__main__":
    matcher = OperatingSystemVersion("android", 11)
    print(repr(matcher))
