from __future__ import annotations

from typing import Literal

from prettyqt import core, qt
from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict


DISCOVERY_METHODS = bidict(
    none=0,  # QtBluetooth.QBluetoothDeviceDiscoveryAgent.NoMethod
    classic=1,  # QtBluetooth.QBluetoothDeviceDiscoveryAgent.ClassicMethod,
    low_energy=2,  # QtBluetooth.QBluetoothDeviceDiscoveryAgent.LowEnergyMethod,
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

    def start_discovery(self, classic: bool = False, low_energy: bool = False):
        flag = 0
        if classic:
            flag &= 1
        if low_energy:
            flag &= 2
        self.start(flag)

    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def get_supported_discovery_methods(self) -> list[DiscoveryMethodStr]:
        return [
            k
            for k, v in DISCOVERY_METHODS.items()
            if v & qt.flag_to_int(self.supportedDiscoveryMethods())
        ]


if __name__ == "__main__":
    agent = BluetoothDeviceDiscoveryAgent()
    print(agent.get_supported_discovery_methods())
