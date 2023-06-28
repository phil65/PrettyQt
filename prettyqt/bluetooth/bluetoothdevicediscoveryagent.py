from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.utils import bidict


DiscoveryMethodStr = Literal["none", "classic", "low_energy"]

DISCOVERY_METHODS: bidict[
    DiscoveryMethodStr, bluetooth.QBluetoothDeviceDiscoveryAgent.DiscoveryMethod
] = bidict(
    none=bluetooth.QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.NoMethod,
    classic=bluetooth.QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.ClassicMethod,
    low_energy=bluetooth.QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod,
)

Error = bluetooth.QBluetoothDeviceDiscoveryAgent.Error

ErrorStr = Literal[
    "none",
    "powered_off",
    "input_output",
    "invalid_bluetooth_adapter",
    "unsupported_platform",
    "unsupported_discovery",
    "unknown",
]

ERROR: bidict[ErrorStr, Error] = bidict(
    none=Error.NoError,
    powered_off=Error.PoweredOffError,
    input_output=Error.InputOutputError,
    invalid_bluetooth_adapter=Error.InvalidBluetoothAdapterError,
    unsupported_platform=Error.UnsupportedPlatformError,
    unsupported_discovery=Error.UnsupportedDiscoveryMethod,
    unknown=Error.UnknownError,
)

# INQUIRY_TYPES = bidict(
#     unlimited=bluetooth.QBluetoothDeviceDiscoveryAgent.GeneralUnlimitedInquiry,
#     limited=bluetooth.QBluetoothDeviceDiscoveryAgent.LimitedInquiry,
# )

# InquiryTypeStr = Literal["unlimited", "limited"]


class BluetoothDeviceDiscoveryAgent(
    core.ObjectMixin, bluetooth.QBluetoothDeviceDiscoveryAgent
):
    device_discovered = core.Signal(object)  # bluetooth.BluetoothDeviceInfo casts signal.

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
    #     """
    #     self.setInquiryType(INQUIRY_TYPES.get_enum_value(typ))

    # def get_inquiry_type(self) -> InquiryTypeStr:
    #     """Get the current inquiry type.

    #     Returns:
    #         inquiry type
    #     """
    #     return INQUIRY_TYPES.inverse[self.inquiryType()]

    def start_discovery(self, classic: bool = True, low_energy: bool = True):
        """Start discovery of bluetooth devices."""
        flag = bluetooth.QBluetoothDeviceDiscoveryAgent.NoMethod
        if classic:
            flag |= bluetooth.QBluetoothDeviceDiscoveryAgent.ClassicMethod
        if low_energy:
            flag |= bluetooth.QBluetoothDeviceDiscoveryAgent.LowEnergyMethod
        self.start(flag)

    def get_error(self) -> ErrorStr:
        """Get error type if available."""
        return ERROR.inverse[self.error()]

    def get_supported_discovery_methods(self) -> list[DiscoveryMethodStr]:
        """Return a list of supported discovery methods."""
        return DISCOVERY_METHODS.get_list(self.supportedDiscoveryMethods())


if __name__ == "__main__":
    import logging

    from prettyqt import core

    app = core.app()
    agent = BluetoothDeviceDiscoveryAgent(app)
    agent.setLowEnergyDiscoveryTimeout(500)
    agent.device_discovered.connect(lambda x: logging.info(x))
    agent.finished.connect(app.quit)
    agent.start_discovery()
    with app.debug_mode():
        app.exec()
