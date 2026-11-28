import json
from typing import Any

from prettyqt import network
from prettyqt.qt import QtNetwork
from prettyqt.utils import get_repr


class RestReply(QtNetwork.QRestReply):
    """Convenience wrapper around QNetworkReply for RESTful operations."""

    def __repr__(self):
        return get_repr(self, self.httpStatus(), self.get_error())

    def __bool__(self) -> bool:
        return self.isSuccess()

    def get_error(self) -> network.networkreply.NetworkErrorStr:
        """Return the network error type as a string."""
        return network.networkreply.NETWORK_ERROR.inverse[self.error()]

    def get_http_status(self) -> int:
        """Return the HTTP status code received in the server response."""
        return self.httpStatus()

    def is_success(self) -> bool:
        """Return whether the request succeeded without network or HTTP error."""
        return self.isSuccess()

    def is_http_status_success(self) -> bool:
        """Return whether the HTTP status code is between 200 and 299."""
        return self.isHttpStatusSuccess()

    def read_text(self) -> str:
        """Read the received data as a string."""
        return self.readText()

    def read_body(self) -> bytes:
        """Read the received data as raw bytes."""
        return bytes(self.readBody().data())

    def read_json(self) -> Any:
        """Read and parse the received JSON data into Python objects, or None."""
        result = self.readJson()
        doc = result[0] if isinstance(result, tuple) else result
        if doc is None or doc.isNull():
            return None
        return json.loads(bytes(doc.toJson().data()).decode())

    def get_network_reply(self) -> network.NetworkReply | None:
        """Return the underlying NetworkReply, or None if unset."""
        reply = self.networkReply()
        return network.NetworkReply(reply) if reply is not None else None
