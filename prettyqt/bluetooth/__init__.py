"""Provides access to Bluetooth hardware."""

from __future__ import annotations

from prettyqt.qt.QtBluetooth import *  # noqa: F403

from .bluetoothdeviceinfo import BluetoothDeviceInfo
from .bluetoothuuid import BluetoothUuid
from .bluetoothaddress import BluetoothAddress
from .bluetoothhostinfo import BluetoothHostInfo
from .bluetoothlocaldevice import BluetoothLocalDevice
from .bluetoothserviceinfo import BluetoothServiceInfo
from .bluetoothsocket import BluetoothSocket
from .bluetoothserver import BluetoothServer
from .bluetoothdevicediscoveryagent import BluetoothDeviceDiscoveryAgent
from .bluetoothservicediscoveryagent import BluetoothServiceDiscoveryAgent
from prettyqt.qt import QtBluetooth

QT_MODULE = QtBluetooth


__all__ = [
    "BluetoothAddress",
    "BluetoothDeviceDiscoveryAgent",
    "BluetoothDeviceInfo",
    "BluetoothHostInfo",
    "BluetoothLocalDevice",
    "BluetoothServer",
    "BluetoothServiceDiscoveryAgent",
    "BluetoothServiceInfo",
    "BluetoothSocket",
    "BluetoothUuid",
]
