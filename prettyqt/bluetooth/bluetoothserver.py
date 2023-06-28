from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.utils import bidict


Error = bluetooth.QBluetoothServer.Error

ErrorStr = Literal[
    "none",
    "unknown",
    "powered_off",
    "input_output",
    "service_already_registered",
    "unsupported_protocol",
    "missing_permissions",
]

ERROR: bidict[ErrorStr, Error] = bidict(
    none=Error.NoError,
    unknown=Error.UnknownError,
    powered_off=Error.PoweredOffError,
    input_output=Error.InputOutputError,
    service_already_registered=Error.ServiceAlreadyRegisteredError,
    unsupported_protocol=Error.UnsupportedProtocolError,
    missing_permissions=Error.MissingPermissionsError,
)



class BluetoothServer(core.ObjectMixin, bluetooth.QBluetoothServer):
    def __init__(
        self,
        protocol: bluetooth.bluetoothserviceinfo.ProtocolStr
        | bluetooth.QBluetoothServiceInfo.Protocol,
        parent: core.QObject | None = None,
    ):
        if isinstance(protocol, str):
            protocol = bluetooth.bluetoothserviceinfo.PROTOCOL[protocol]
        super().__init__(protocol, parent)

    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def get_server_type(self) -> bluetooth.bluetoothserviceinfo.ProtocolStr:
        return bluetooth.bluetoothserviceinfo.PROTOCOL.inverse[self.serverType()]

    def get_server_address(self) -> bluetooth.BluetoothAddress:
        return bluetooth.BluetoothAddress(self.serverAddress())


if __name__ == "__main__":
    from prettyqt import core

    app = core.app()
    server = BluetoothServer("l2_cap")
    with app.debug_mode():
        app.exec()
