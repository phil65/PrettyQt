from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


CommunicationModeStr = Literal["access", "advertise"]

COMMUNICATION_MODE: bidict[
    CommunicationModeStr, QtCore.QBluetoothPermission.CommunicationMode
] = bidict(
    access=QtCore.QBluetoothPermission.CommunicationMode.Access,
    advertise=QtCore.QBluetoothPermission.CommunicationMode.Advertise,
)


class BluetoothPermission(QtCore.QBluetoothPermission):
    """Access Bluetooth peripherals."""

    def set_communication_modes(
        self,
        modes: CommunicationModeStr | QtCore.QBluetoothPermission.CommunicationMode,
    ):
        """Set the Bluetooth communication modes.

        Args:
            modes: communication modes to set
        """
        self.setCommunicationModes(COMMUNICATION_MODE.get_enum_value(modes))

    def get_communication_modes(self) -> list[CommunicationModeStr]:
        """Return the active Bluetooth communication modes.

        Returns:
            list of communication modes
        """
        modes = self.communicationModes()
        return [k for k, v in COMMUNICATION_MODE.items() if v.value & modes.value]
