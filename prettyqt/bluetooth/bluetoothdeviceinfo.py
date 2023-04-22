from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict


mod = QtBluetooth.QBluetoothDeviceInfo

CORE_CONFIGURATION = bidict(
    none=mod.CoreConfiguration.UnknownCoreConfiguration,
    base_rate=mod.CoreConfiguration.BaseRateCoreConfiguration,
    base_rate_and_low_energy=mod.CoreConfiguration.BaseRateAndLowEnergyCoreConfiguration,
    low_energy=mod.CoreConfiguration.LowEnergyCoreConfiguration,
)

CoreConfigurationStr = Literal[
    "none", "base_rate", "base_rate_and_low_energy", "low_energy"
]

FIELD = bidict(
    none=mod.Field(0),
    rssi=mod.Field.RSSI,
    manufacturer_data=mod.Field.ManufacturerData,
    service_data=mod.Field.ServiceData,
)

FieldStr = Literal[
    "none",
    "rssi",
    "manufacturer_data",
    "service_data",
]

MAJOR_DEVICE_CLASS = bidict(
    miscellaneous=mod.MajorDeviceClass.MiscellaneousDevice,
    computer=mod.MajorDeviceClass.ComputerDevice,
    phone=mod.MajorDeviceClass.PhoneDevice,
    network=mod.MajorDeviceClass.NetworkDevice,
    audio_video=mod.MajorDeviceClass.AudioVideoDevice,
    peripheral=mod.MajorDeviceClass.PeripheralDevice,
    imaging=mod.MajorDeviceClass.ImagingDevice,
    wearable=mod.MajorDeviceClass.WearableDevice,
    toy=mod.MajorDeviceClass.ToyDevice,
    health=mod.MajorDeviceClass.HealthDevice,
    uncategorized=mod.MajorDeviceClass.UncategorizedDevice,
)

MajorDeviceClassStr = Literal[
    "none",
    "rssi",
    "manufacturer_data",
    "service_data",
    "service_data",
    "service_data",
    "service_data",
    "service_data",
    "service_data",
    "service_data",
    "service_data",
]

class BluetoothDeviceInfo(QtBluetooth.QBluetoothDeviceInfo):
    def __repr__(self):
        return f"{type(self).__name__}('{self.get_address()}')"

    def __bool__(self):
        return self.isValid()

    def get_address(self) -> bluetooth.BluetoothAddress:
        return bluetooth.BluetoothAddress(self.address())

    def get_service_ids(self) -> list[bluetooth.BluetoothUuid]:
        return [bluetooth.BluetoothUuid(i) for i in self.serviceIds()]

    def get_service_uuids(self) -> list[bluetooth.BluetoothUuid]:
        return [bluetooth.BluetoothUuid(i) for i in self.serviceUuids()]



if __name__ == "__main__":
    from prettyqt import core

    app = core.app()
    info = BluetoothDeviceInfo()
    print(info)
