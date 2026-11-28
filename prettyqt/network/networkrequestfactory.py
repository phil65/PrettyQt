from collections.abc import Mapping
from typing import Any

from prettyqt import core, network
from prettyqt.qt import QtNetwork
from prettyqt.utils import datatypes, get_repr


class NetworkRequestFactory(QtNetwork.QNetworkRequestFactory):
    """Convenience class for creating QNetworkRequest objects with shared settings."""

    def __init__(
        self,
        obj: datatypes.UrlType | QtNetwork.QNetworkRequestFactory | None = None,
    ):
        if isinstance(obj, QtNetwork.QNetworkRequestFactory):
            super().__init__(obj)
        else:
            super().__init__()
            if obj is not None:
                self.set_base_url(obj)

    def __repr__(self):
        return get_repr(self, self.get_base_url())

    def set_base_url(self, url: datatypes.UrlType):
        """Set the base URL used to populate request URLs."""
        self.setBaseUrl(datatypes.to_url(url))

    def get_base_url(self) -> core.Url:
        """Return the base URL used to populate request URLs."""
        return core.Url(self.baseUrl())

    def set_common_headers(self, headers: QtNetwork.QHttpHeaders | Mapping[str, str]):
        """Set headers common to all requests created by this factory."""
        if isinstance(headers, Mapping):
            headers = network.HttpHeaders.from_dict(headers)
        self.setCommonHeaders(headers)

    def get_common_headers(self) -> network.HttpHeaders:
        """Return headers common to all requests created by this factory."""
        return network.HttpHeaders(self.commonHeaders())

    def set_bearer_token(self, token: datatypes.ByteArrayType):
        """Set the bearer token for requests created by this factory."""
        self.setBearerToken(datatypes.to_bytearray(token))

    def get_bearer_token(self) -> str:
        """Return the bearer token as a decoded string."""
        return bytes(self.bearerToken().data()).decode()

    def set_priority(
        self,
        priority: network.networkrequest.PriorityStr | QtNetwork.QNetworkRequest.Priority,
    ):
        """Set priority for requests created by this factory."""
        self.setPriority(network.networkrequest.PRIORITY.get_enum_value(priority))

    def get_priority(self) -> network.networkrequest.PriorityStr:
        """Return priority for requests created by this factory."""
        return network.networkrequest.PRIORITY.inverse[self.priority()]

    def set_attribute(
        self,
        attribute: network.networkrequest.AttributeStr
        | QtNetwork.QNetworkRequest.Attribute,
        value: datatypes.Variant,
    ):
        """Set an attribute common to all requests created by this factory."""
        self.setAttribute(
            network.networkrequest.ATTRIBUTE.get_enum_value(attribute), value
        )

    def get_attribute(
        self,
        attribute: network.networkrequest.AttributeStr
        | QtNetwork.QNetworkRequest.Attribute,
        default: Any = None,
    ) -> Any:
        """Return the value of the given attribute, or default if not set."""
        return self.attribute(
            network.networkrequest.ATTRIBUTE.get_enum_value(attribute), default
        )

    def clear_attribute(
        self,
        attribute: network.networkrequest.AttributeStr
        | QtNetwork.QNetworkRequest.Attribute,
    ):
        """Clear the given attribute from this factory."""
        self.clearAttribute(network.networkrequest.ATTRIBUTE.get_enum_value(attribute))

    def create_request(
        self,
        path: str | None = None,
        query: core.QUrlQuery | None = None,
    ) -> network.NetworkRequest:
        """Create a NetworkRequest from base URL, optional path, and optional query."""
        if path is not None and query is not None:
            req = self.createRequest(path, query)
        elif path is not None:
            req = self.createRequest(path)
        elif query is not None:
            req = self.createRequest(query)
        else:
            req = self.createRequest()
        return network.NetworkRequest(req)


if __name__ == "__main__":
    factory = NetworkRequestFactory("https://example.com/api")
    print(repr(factory))
