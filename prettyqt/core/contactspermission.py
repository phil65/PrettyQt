from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


AccessModeStr = Literal["read_only", "read_write"]

ACCESS_MODE: bidict[AccessModeStr, QtCore.QContactsPermission.AccessMode] = bidict(
    read_only=QtCore.QContactsPermission.AccessMode.ReadOnly,
    read_write=QtCore.QContactsPermission.AccessMode.ReadWrite,
)


class ContactsPermission(QtCore.QContactsPermission):
    """Access the user's contacts."""

    def set_access_mode(
        self, mode: AccessModeStr | QtCore.QContactsPermission.AccessMode
    ):
        """Set the contacts access mode.

        Args:
            mode: access mode to use
        """
        self.setAccessMode(ACCESS_MODE.get_enum_value(mode))

    def get_access_mode(self) -> AccessModeStr:
        """Return current contacts access mode.

        Returns:
            access mode
        """
        return ACCESS_MODE.inverse[self.accessMode()]
