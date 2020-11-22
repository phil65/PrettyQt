#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

# import pytest

from prettyqt import bluetooth

# from prettyqt.utils import InvalidParamError


def test_bluetoothaddress():
    address = bluetooth.BluetoothAddress()
    repr(address)
    assert not address


def test_bluetoothservicediscoveryagent(qtlog):
    with qtlog.disabled():
        agent = bluetooth.BluetoothServiceDiscoveryAgent()
    assert agent.get_error() == "none"
    assert agent.get_discovered_services() == []


def test_bluetoothdevicediscoveryagent():
    agent = bluetooth.BluetoothDeviceDiscoveryAgent()
    assert agent.get_error() == "none"
    agent.get_supported_discovery_methods()
