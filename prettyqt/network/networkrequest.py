# -*- coding: utf-8 -*-

from typing import Union, Dict

from qtpy import QtNetwork, QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

KNOWN_HEADERS = bidict(
    content_disposition=QtNetwork.QNetworkRequest.ContentDispositionHeader,
    content_type=QtNetwork.QNetworkRequest.ContentTypeHeader,
    content_length=QtNetwork.QNetworkRequest.ContentLengthHeader,
    location=QtNetwork.QNetworkRequest.LocationHeader,
    last_modified=QtNetwork.QNetworkRequest.LastModifiedHeader,
    if_modified_since=QtNetwork.QNetworkRequest.IfModifiedSinceHeader,
    etag=QtNetwork.QNetworkRequest.ETagHeader,
    if_match=QtNetwork.QNetworkRequest.IfMatchHeader,
    if_none_match=QtNetwork.QNetworkRequest.IfNoneMatchHeader,
    cookie=QtNetwork.QNetworkRequest.CookieHeader,
    set_cooke=QtNetwork.QNetworkRequest.SetCookieHeader,
    user_agent=QtNetwork.QNetworkRequest.UserAgentHeader,
    server=QtNetwork.QNetworkRequest.ServerHeader,
)

PRIORITIES = bidict(
    high=QtNetwork.QNetworkRequest.HighPriority,
    normal=QtNetwork.QNetworkRequest.NormalPriority,
    low=QtNetwork.QNetworkRequest.LowPriority,
)

REDIRECT_POLICIES = bidict(
    manual=QtNetwork.QNetworkRequest.ManualRedirectPolicy,
    no_less_safe=QtNetwork.QNetworkRequest.NoLessSafeRedirectPolicy,
    same_origin=QtNetwork.QNetworkRequest.SameOriginRedirectPolicy,
    user_verified=QtNetwork.QNetworkRequest.UserVerifiedRedirectPolicy,
)

CACHE_LOAD_CONTROL = bidict(
    always_network=QtNetwork.QNetworkRequest.AlwaysNetwork,
    prefer_network=QtNetwork.QNetworkRequest.PreferNetwork,
    prefer_cache=QtNetwork.QNetworkRequest.PreferCache,
    always_cache=QtNetwork.QNetworkRequest.AlwaysCache,
)


class NetworkRequest(QtNetwork.QNetworkRequest):
    def __init__(self, obj: Union[QtCore.QUrl, str, QtNetwork.QNetworkRequest] = None):
        if isinstance(obj, QtNetwork.QNetworkRequest):
            super().__init__(obj)
        else:
            super().__init__()
            if obj is not None:
                self.set_url(obj)

    def __repr__(self):
        return f"NetworkRequest({self.get_url()})"

    def set_headers(self, headers: Dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(str.encode(k), str.encode(v))

    def get_headers(self) -> Dict[str, str]:
        return {
            bytes(h).decode(): bytes(self.rawHeader(h)).decode()
            for h in self.rawHeaderList()
        }

    def set_url(self, url: Union[str, QtCore.QUrl]):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def set_priority(self, priority: str):
        """Set priority.

        Valid values for priority: "high", "normal", "low"

        Args:
            priority: priority

        Raises:
            InvalidParamError: priority does not exist
        """
        if priority not in PRIORITIES:
            raise InvalidParamError(priority, PRIORITIES)
        self.setPriority(PRIORITIES[priority])

    def get_priority(self) -> str:
        """Get the current priority.

        Possible values: "high", "normal", "low"

        Returns:
            priority
        """
        return PRIORITIES.inv[self.priority()]
