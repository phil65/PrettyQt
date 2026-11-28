from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


AccessModeStr = Literal["read_only", "read_write", "write_only"]

ACCESS_MODE: bidict[AccessModeStr, QtCore.QCalendarPermission.AccessMode] = bidict(
    read_only=QtCore.QCalendarPermission.AccessMode.ReadOnly,
    read_write=QtCore.QCalendarPermission.AccessMode.ReadWrite,
    write_only=QtCore.QCalendarPermission.AccessMode.WriteOnly,
)


class CalendarPermission(QtCore.QCalendarPermission):
    """Access the user's calendar."""

    def set_access_mode(
        self, mode: AccessModeStr | QtCore.QCalendarPermission.AccessMode
    ):
        """Set the calendar access mode.

        Args:
            mode: access mode to use
        """
        self.setAccessMode(ACCESS_MODE.get_enum_value(mode))

    def get_access_mode(self) -> AccessModeStr:
        """Return current calendar access mode.

        Returns:
            access mode
        """
        return ACCESS_MODE.inverse[self.accessMode()]
