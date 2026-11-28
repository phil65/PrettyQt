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
    info = bluetooth.BluetoothDeviceInfo()
    info.get_device_uuid()
    assert info.get_major_device_class() == "miscellaneous"
    assert info.get_minor_device_class() == "uncategorized"


def test_bluetooth_enums_and_service_info():
    assert "all" in bluetooth.bluetoothdeviceinfo.FIELD
    assert "location_service_turned_off" in bluetooth.bluetoothdevicediscoveryagent.ERROR
    assert "missing_permissions" in bluetooth.bluetoothdevicediscoveryagent.ERROR
    assert "missing_permissions" in bluetooth.bluetoothservicediscoveryagent.ERRORS

    info = bluetooth.BluetoothServiceInfo()
    assert "service_availability" in bluetooth.bluetoothserviceinfo.ATTRIBUTE_IDS
    assert "nonexistent_key" not in info
    info["service_info_time_to_live"] = 42
    assert "service_info_time_to_live" in info
    assert info["service_info_time_to_live"] == 42  # noqa: PLR2004
    del info["service_info_time_to_live"]
    assert "service_info_time_to_live" not in info
    with pytest.raises(KeyError):
        info[object()] = "x"  # type: ignore[index]
    with pytest.raises(KeyError):
        del info[object()]  # type: ignore[arg-type]


def test_bluetooth_socket_and_uuid():
    sock = bluetooth.BluetoothSocket()
    assert sock.get_socket_type() == "unknown"
    rfcomm_sock = bluetooth.BluetoothSocket("rfcomm")
    assert rfcomm_sock.get_socket_type() == "rfcomm"
    assert bluetooth.BluetoothUuid.characteristic_to_string("magnetic_flux_density_3d")
    assert bluetooth.BluetoothUuid.protocol_to_string("rfcomm")
    assert hasattr(bluetooth.bluetoothuuid, "ProtocolUuidStr")
