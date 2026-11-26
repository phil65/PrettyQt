"""Tests for `prettyqt` package."""

import pytest


bluetooth = pytest.importorskip("prettyqt.bluetooth")

# from prettyqt.utils import InvalidParamError


def test_bluetoothaddress():
    address = bluetooth.BluetoothAddress()
    repr(address)
    assert not address


def test_bluetoothservicediscoveryagent():
    agent = bluetooth.BluetoothServiceDiscoveryAgent()
    assert agent.get_error() == "none"
    assert agent.get_discovered_services() == []


def test_bluetoothdevicediscoveryagent():
    agent = bluetooth.BluetoothDeviceDiscoveryAgent()
    assert agent.get_error() == "none"
    agent.get_supported_discovery_methods()


def test_bluetooth_discovery_and_host_mode(qapp):
    agent = bluetooth.BluetoothDeviceDiscoveryAgent()
    agent.start_discovery(classic=True, low_energy=False)
    agent.stop()
    service_agent = bluetooth.BluetoothServiceDiscoveryAgent()
    service_agent.start_discovery(full=True)
    service_agent.stop()
    device = bluetooth.BluetoothLocalDevice()
    device.get_host_mode()
    bluetooth.BluetoothDeviceInfo().get_device_uuid()
