from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict


DISCOVERY_METHODS = bidict(
    none=QtBluetooth.QBluetoothDeviceDiscoveryAgent.NoMethod,
    classic=QtBluetooth.QBluetoothDeviceDiscoveryAgent.ClassicMethod,
    low_energy=QtBluetooth.QBluetoothDeviceDiscoveryAgent.LowEnergyMethod,
)

DiscoveryMethodStr = Literal["none", "classic", "low_energy"]

module = QtBluetooth.QBluetoothDeviceDiscoveryAgent

ERROR = bidict(
    none=module.NoError,
    powered_off=module.PoweredOffError,
    input_output=module.InputOutputError,
    invalid_bluetooth_adapter=module.InvalidBluetoothAdapterError,
    unsupported_platform=module.UnsupportedPlatformError,
    unsupported_discovery=module.UnsupportedDiscoveryMethod,
    unknown=module.UnknownError,
)

ErrorStr = Literal[
    "none",
    "powered_off",
    "input_output",
    "invalid_bluetooth_adapter",
    "unsupported_platform",
    "unsupported_discovery",
    "unknown",
]

# INQUIRY_TYPES = bidict(
#     unlimited=QtBluetooth.QBluetoothDeviceDiscoveryAgent.GeneralUnlimitedInquiry,
#     limited=QtBluetooth.QBluetoothDeviceDiscoveryAgent.LimitedInquiry,
# )

# InquiryTypeStr = Literal["unlimited", "limited"]


class BluetoothDeviceDiscoveryAgent(
    core.ObjectMixin, QtBluetooth.QBluetoothDeviceDiscoveryAgent
):
    device_discovered = core.Signal(bluetooth.BluetoothDeviceInfo)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deviceDiscovered.connect(self._on_device_discovered)

    def _on_device_discovered(self, info):
        info = bluetooth.BluetoothDeviceInfo(info)
        self.device_discovered.emit(info)

    # def set_inquiry_type(self, typ: InquiryTypeStr):
    #     """Set inquiry type.

    #     Args:
    #         typ: inquiry type

    #     Raises:
    #         InvalidParamError: inquiry type does not exist
    #     """
    #     if typ not in INQUIRY_TYPES:
    #         raise InvalidParamError(typ, INQUIRY_TYPES)
    #     self.setInquiryType(INQUIRY_TYPES[typ])

    # def get_inquiry_type(self) -> InquiryTypeStr:
    #     """Get the current inquiry type.

    #     Returns:
    #         inquiry type
    #     """
    #     return INQUIRY_TYPES.inverse[self.inquiryType()]

    def start_discovery(self, classic: bool = True, low_energy: bool = True):
        flag = QtBluetooth.QBluetoothDeviceDiscoveryAgent.NoMethod
        if classic:
            flag |= QtBluetooth.QBluetoothDeviceDiscoveryAgent.ClassicMethod
        if low_energy:
            flag |= QtBluetooth.QBluetoothDeviceDiscoveryAgent.LowEnergyMethod
        self.start(flag)

    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def get_supported_discovery_methods(self) -> list[DiscoveryMethodStr]:
        return DISCOVERY_METHODS.get_list(self.supportedDiscoveryMethods())


if __name__ == "__main__":
    import logging
    import sys

    from prettyqt import core

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    app = core.app()
    agent = BluetoothDeviceDiscoveryAgent(app)
    agent.setLowEnergyDiscoveryTimeout(500)
    # agent.device_discovered.connect(lambda device: logging.info(type(device)))
    agent.finished.connect(app.quit)
    agent.start_discovery()
    app.main_loop()
