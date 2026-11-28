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
    with pytest.raises(InvalidParamError):
        part.set_header("invalid", "c")


def test_localserver():
    server = network.LocalServer()
    assert server.get_server_error() == "unknown_socket"
    server.set_socket_options("user")
    assert server.get_socket_options() == ["user", "world"]
    assert "abstract_namespace" in network.localserver.SOCKET_OPTION


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
    assert "set_cookie" in network.networkrequest.KNOWN_HEADER
    assert "full_local_server_name" in network.networkrequest.ATTRIBUTE
    assert "operation_canceled" in network.networkreply.NETWORK_ERROR
    assert "datagram_too_large" in network.abstractsocket.SOCKET_ERROR
    assert "keep_alive_count" in network.abstractsocket.SOCKET_OPTION
    assert "keep_alive_idle" in network.abstractsocket.SOCKET_OPTION
    assert "keep_alive_interval" in network.abstractsocket.SOCKET_OPTION


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
    assert cookie.to_raw_form(full=False) == b"test=testus"
    cookie.set_same_site_policy("strict")
    assert cookie.get_same_site_policy() == "strict"
    with pytest.raises(InvalidParamError):
        cookie.set_same_site_policy("invalid")
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
    assert server.listen()
    server.close()
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


def test_httpheaders():
    headers = network.HttpHeaders()
    assert not headers
    assert len(headers) == 0
    headers.append_header("content_type", "application/json")
    headers.append_header("X-Custom", "value1")
    headers.append_header("X-Custom", "value2")
    assert bool(headers)
    assert len(headers) == 3  # noqa: PLR2004
    assert "content_type" in headers
    assert "Content-Type" in headers
    assert "X-Custom" in headers
    assert "missing" not in headers
    assert headers["content_type"] == "application/json"
    assert headers.get_value("content_type") == "application/json"
    assert headers.get_value("missing", "fallback") == "fallback"
    assert headers.get_values("X-Custom") == ["value1", "value2"]
    assert headers.get_combined_value("X-Custom") == "value1, value2"
    headers["X-Custom"] = "replaced"
    assert headers["X-Custom"] == "replaced"
    del headers["X-Custom"]
    assert "X-Custom" not in headers
    with pytest.raises(KeyError):
        _ = headers["missing"]
    with pytest.raises(KeyError):
        del headers["missing"]
    assert headers.to_dict() == {"content-type": "application/json"}
    assert headers.to_list() == [("content-type", "application/json")]
    repr(headers)
    from_dict = network.HttpHeaders.from_dict({"accept": "text/plain", "X-A": "1"})
    assert from_dict["accept"] == "text/plain"
    assert from_dict["X-A"] == "1"
    assert "content_type" in network.httpheaders.WELL_KNOWN_HEADER


def test_networkrequestfactory():
    factory = network.NetworkRequestFactory("https://example.com/api")
    assert factory.get_base_url() == core.Url("https://example.com/api")
    factory.set_base_url("https://api.example.org/v1")
    assert factory.get_base_url() == core.Url("https://api.example.org/v1")
    factory.set_common_headers({"content_type": "application/json", "X-Key": "abc"})
    common = factory.get_common_headers()
    assert isinstance(common, network.HttpHeaders)
    assert common["content_type"] == "application/json"
    assert common["X-Key"] == "abc"
    factory.set_bearer_token("secret-token")
    assert factory.get_bearer_token() == "secret-token"
    factory.set_priority("high")
    assert factory.get_priority() == "high"
    with pytest.raises(InvalidParamError):
        factory.set_priority("invalid")
    factory.set_attribute("http2_allowed", False)
    assert factory.get_attribute("http2_allowed") is False
    factory.clear_attribute("http2_allowed")
    assert factory.get_attribute("http2_allowed", "default") == "default"
    req = factory.create_request("users")
    assert isinstance(req, network.NetworkRequest)
    assert req.get_url() == core.Url("https://api.example.org/v1/users")
    query = core.QUrlQuery()
    query.addQueryItem("page", "2")
    req_q = factory.create_request("users", query)
    assert req_q.get_url() == core.Url("https://api.example.org/v1/users?page=2")
    req_only_q = factory.create_request(query=query)
    assert req_only_q.get_url() == core.Url("https://api.example.org/v1?page=2")
    req_base = factory.create_request()
    assert req_base.get_url() == core.Url("https://api.example.org/v1")
    repr(factory)


def test_restaccessmanager_and_restreply(qapp):
    nam = network.NetworkAccessManager()
    rest = network.RestAccessManager(nam)
    assert rest.get_network_access_manager() is nam
    reply = network.RestReply(None)  # ty: ignore[invalid-argument-type]
    assert not reply
    assert reply.is_success() is False
    assert reply.is_http_status_success() is False
    assert reply.get_http_status() == 0
    assert reply.get_error() == "none"
    assert reply.read_text() == ""
    assert reply.read_body() == b""
    assert reply.read_json() is None
    assert reply.get_network_reply() is None
    repr(reply)
