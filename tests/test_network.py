"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core, network
from prettyqt.utils import InvalidParamError


def test_hostaddress():
    address = network.HostAddress()
    address.set_address("localhost")
    repr(address)
    assert str(address) in ["0.0.0.2", "127.0.0.1"]
    assert address.get_protocol() == "ipv4"


def test_httppart():
    part = network.HttpPart()
    part.set_body("test")
    part.set_headers(dict(a="b"))
    part.set_header("location", "c")


def test_localserver():
    server = network.LocalServer()
    assert server.get_server_error() == "unknown_socket"
    server.set_socket_options("user")
    assert server.get_socket_options() == ["user", "world"]


def test_httpmultipart():
    part = network.HttpMultiPart()
    part.set_content_type("related")
    with pytest.raises(InvalidParamError):
        part.set_content_type("test")
    part.set_boundary("test")
    assert part.get_boundary() == "test"


def test_networkaddressentry():
    entry = network.NetworkAddressEntry()
    entry.set_dns_eligibility("eligible")
    with pytest.raises(InvalidParamError):
        entry.set_dns_eligibility("test")
    assert entry.get_dns_eligibility() == "eligible"
    entry.set_ip("123.123.123.123")
    assert entry.get_ip() == network.HostAddress("123.123.123.123")
    entry.set_netmask("255.255.255.255")
    assert entry.get_netmask() == network.HostAddress("255.255.255.255")
    entry.get_preferred_lifetime()
    entry.get_validity_lifetime()


def test_networkdatagram():
    datagram = network.NetworkDatagram()
    datagram.get_destination_address()
    datagram.get_sender_address()
    datagram.set_data("test")
    assert datagram.get_data() == "test"


def test_networkinterface():
    interface = network.NetworkInterface()
    interface.get_address_entries()
    network.NetworkInterface.get_all_addresses()
    network.NetworkInterface.get_all_interfaces()
    network.NetworkInterface.get_interface_from_name("test")
    assert interface.get_type() == "unknown"


def test_networkproxy():
    proxy = network.NetworkProxy()
    proxy.set_capabilities("listening")
    assert proxy.get_capabilities() == ["listening"]
    proxy.set_type("http_caching")
    with pytest.raises(InvalidParamError):
        proxy.set_type("test")
    assert proxy.get_type() == "http_caching"
    headers = {"a": "b"}
    proxy.set_headers(headers)
    assert proxy.get_headers() == headers
    with pytest.raises(InvalidParamError):
        proxy.set_header("test", "test")
    proxy.set_header("location", "test")
    with pytest.raises(InvalidParamError):
        proxy.get_header("test")
    assert proxy.get_header("location") == "test"


def test_networkrequest():
    req = network.NetworkRequest()
    headers = {"a": "b"}
    req.set_headers(headers)
    assert req.get_headers() == headers
    req.set_priority("low")
    assert req.get_priority() == "low"
    req.set_url("http://www.google.de")
    assert req.get_url() == core.Url("http://www.google.de")
    with pytest.raises(InvalidParamError):
        req.set_header("test", "test")
    req.set_header("location", "test")
    with pytest.raises(InvalidParamError):
        req.get_header("test")
    assert req.get_header("location") == "test"


def test_networkaccessmanager():
    manager = network.NetworkAccessManager()
    manager.set_redirect_policy("no_less_safe")
    with pytest.raises(InvalidParamError):
        manager.set_redirect_policy("test")
    assert manager.get_redirect_policy() == "no_less_safe"


def test_networkcookie():
    cookie = network.NetworkCookie()
    cookie.set_name("test")
    assert cookie.get_name() == "test"
    cookie.set_value("testus")
    assert cookie.get_value() == "testus"
    assert cookie.to_raw_form(full=False) is None
    cookie.set_expiration_date(None)


def test_networkcookiejar():
    jar = network.NetworkCookieJar()
    assert jar["test"] == []
    for _i in jar:
        pass
    repr(jar)
    jar += network.NetworkCookie()
    jar.set_cookies_from_url([], "http://www.google.de")


def test_udpsocket():
    socket = network.UdpSocket()
    socket.bind_to("localhost")
    socket.get_multicast_interface()
    socket.receive_datagram()


def test_tcpserver():
    server = network.TcpServer()
    server.get_server_address()
    server.get_proxy()
    assert server.get_server_error() == "unknown_socket"


def test_tcpsocket():
    socket = network.TcpSocket()
    socket.set_pause_mode("on_ssl_errors")
    with pytest.raises(InvalidParamError):
        socket.set_pause_mode("test")
    assert socket.get_pause_mode() == "on_ssl_errors"
    assert socket.get_error() == "unknown_socket"
    socket.get_proxy()
    # socket.set_socket_option("low_delay", 1)
    # assert socket.get_socket_option("low_delay") == 1
    # socket.set_type_of_service("priority")
    # assert socket.get_type_of_service() == "priority"
    assert socket.get_socket_type() == "tcp"
    assert socket.get_state() == "unconnected"
    assert not socket.get_local_address()
