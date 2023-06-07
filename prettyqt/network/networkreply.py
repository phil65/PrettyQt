from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import bidict


NETWORK_ERROR = bidict(
    none=QtNetwork.QNetworkReply.NetworkError.NoError,
    connection_refused=QtNetwork.QNetworkReply.NetworkError.ConnectionRefusedError,
    remote_host_closed=QtNetwork.QNetworkReply.NetworkError.RemoteHostClosedError,
    host_not_found=QtNetwork.QNetworkReply.NetworkError.HostNotFoundError,
    timeout=QtNetwork.QNetworkReply.NetworkError.TimeoutError,
    operaion_canceled=QtNetwork.QNetworkReply.NetworkError.OperationCanceledError,
    ssl_handshake_failed=QtNetwork.QNetworkReply.NetworkError.SslHandshakeFailedError,
    temporary_network_failure=QtNetwork.QNetworkReply.NetworkError.TemporaryNetworkFailureError,
    network_session_failed=QtNetwork.QNetworkReply.NetworkError.NetworkSessionFailedError,
    background_request_not_allowed=QtNetwork.QNetworkReply.NetworkError.BackgroundRequestNotAllowedError,
    too_many_redirects=QtNetwork.QNetworkReply.NetworkError.TooManyRedirectsError,
    insecure_redirect=QtNetwork.QNetworkReply.NetworkError.InsecureRedirectError,
    proxy_connection_refused=QtNetwork.QNetworkReply.NetworkError.ProxyConnectionRefusedError,
    proxy_connection_closed=QtNetwork.QNetworkReply.NetworkError.ProxyConnectionClosedError,
    proxy_not_found=QtNetwork.QNetworkReply.NetworkError.ProxyNotFoundError,
    proxy_timeout=QtNetwork.QNetworkReply.NetworkError.ProxyTimeoutError,
    proxy_authentication_required=QtNetwork.QNetworkReply.NetworkError.ProxyAuthenticationRequiredError,
    content_access_denied=QtNetwork.QNetworkReply.NetworkError.ContentAccessDenied,
    content_operation_not_permitted=QtNetwork.QNetworkReply.NetworkError.ContentOperationNotPermittedError,
    content_not_found=QtNetwork.QNetworkReply.NetworkError.ContentNotFoundError,
    authentication_required=QtNetwork.QNetworkReply.NetworkError.AuthenticationRequiredError,
    content_resend=QtNetwork.QNetworkReply.NetworkError.ContentReSendError,
    content_conflict=QtNetwork.QNetworkReply.NetworkError.ContentConflictError,
    content_gone=QtNetwork.QNetworkReply.NetworkError.ContentGoneError,
    internal_server=QtNetwork.QNetworkReply.NetworkError.InternalServerError,
    operation_not_implemented=QtNetwork.QNetworkReply.NetworkError.OperationNotImplementedError,
    service_unavailable=QtNetwork.QNetworkReply.NetworkError.ServiceUnavailableError,
    protocol_unknown=QtNetwork.QNetworkReply.NetworkError.ProtocolUnknownError,
    protocol_invalid_operation=QtNetwork.QNetworkReply.NetworkError.ProtocolInvalidOperationError,
    unknown_network=QtNetwork.QNetworkReply.NetworkError.UnknownNetworkError,
    unknown_proxy=QtNetwork.QNetworkReply.NetworkError.UnknownProxyError,
    unknown_content=QtNetwork.QNetworkReply.NetworkError.UnknownContentError,
    protocol_failure=QtNetwork.QNetworkReply.NetworkError.ProtocolFailure,
    unknown_server=QtNetwork.QNetworkReply.NetworkError.UnknownServerError,
)

NetworkErrorStr = Literal[
    "none",
    "connection_refused",
    "remote_host_closed",
    "host_not_found",
    "timeout",
    "operaion_canceled",
    "ssl_handshake_failed",
    "temporary_network_failure",
    "network_session_failed",
    "background_request_not_allowed",
    "too_many_redirects",
    "insecure_redirect",
    "proxy_connection_refused",
    "proxy_connection_closed",
    "proxy_not_found",
    "proxy_timeout",
    "proxy_authentication_required",
    "content_access_denied",
    "content_operation_not_permitted",
    "content_not_found",
    "authentication_required",
    "content_resend",
    "content_conflict",
    "content_gone",
    "internal_server",
    "operation_not_implemented",
    "service_unavailable",
    "protocol_unknown",
    "protocol_invalid_operation",
    "unknown_network",
    "unknown_proxy",
    "unknown_content",
    "protocol_failure",
    "unknown_server",
]


class NetworkReply:
    def __init__(self, reply: QtNetwork.QNetworkReply):
        self.item = reply

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_error(self) -> NetworkErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return NETWORK_ERROR.inverse[self.error()]

    def set_raw_headers(self, headers: dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(
                QtCore.QByteArray(k.encode()), QtCore.QByteArray(v.encode())
            )

    def get_raw_headers(self) -> dict[str, str]:
        return {
            h.data().decode(): self.rawHeader(h).data().decode()
            for h in self.rawHeaderList()
        }
