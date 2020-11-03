from typing import List

from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtBluetooth
elif PYSIDE2:
    from PySide2 import QtBluetooth

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


DISCOVERY_METHODS = bidict(
    none=0,  # QtBluetooth.QBluetoothDeviceDiscoveryAgent.NoMethod
    classic=1,  # QtBluetooth.QBluetoothDeviceDiscoveryAgent.ClassicMethod,
    low_energy=2,  # QtBluetooth.QBluetoothDeviceDiscoveryAgent.LowEnergyMethod,
)

module = QtBluetooth.QBluetoothDeviceDiscoveryAgent

ERRORS = bidict(
    none=module.NoError,
    powered_off=module.PoweredOffError,
    input_output=module.InputOutputError,
    invalid_bluetooth_adapter=module.InvalidBluetoothAdapterError,
    unsupported_platform=module.UnsupportedPlatformError,
    unsupported_discovery=module.UnsupportedDiscoveryMethod,
    unknown=module.UnknownError,
)

INQUIRY_TYPES = bidict(
    unlimited=QtBluetooth.QBluetoothDeviceDiscoveryAgent.GeneralUnlimitedInquiry,
    limited=QtBluetooth.QBluetoothDeviceDiscoveryAgent.LimitedInquiry,
)


QtBluetooth.QBluetoothDeviceDiscoveryAgent.__bases__ = (core.Object,)


class BluetoothDeviceDiscoveryAgent(QtBluetooth.QBluetoothDeviceDiscoveryAgent):
    def set_inquiry_type(self, typ: str):
        """Set inquiry type.

        Valid values: "unlimited", "limited"

        Args:
            typ: inquiry type

        Raises:
            InvalidParamError: inquiry type does not exist
        """
        if typ not in INQUIRY_TYPES:
            raise InvalidParamError(typ, INQUIRY_TYPES)
        self.setInquiryType(INQUIRY_TYPES[typ])

    def get_inquiry_type(self) -> str:
        """Get the current inquiry type.

        Possible values: "unlimited", "limited"

        Returns:
            inquiry type
        """
        return INQUIRY_TYPES.inv[self.inquiryType()]

    def start_discovery(self, classic: bool = False, low_energy: bool = False):
        flag = 0
        if classic:
            flag &= 1
        if low_energy:
            flag &= 2
        self.start(flag)

    def get_error(self) -> str:
        return ERRORS.inv[self.error()]

    def get_supported_discovery_methods(self) -> List[str]:
        return [
            k
            for k, v in DISCOVERY_METHODS.items()
            if v & int(self.supportedDiscoveryMethods())
        ]


if __name__ == "__main__":
    agent = BluetoothDeviceDiscoveryAgent()
    print(agent.get_supported_discovery_methods())
