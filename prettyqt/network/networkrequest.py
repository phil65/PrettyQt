from typing import Dict, Literal, Optional, Union

from qtpy import QtCore, QtNetwork

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


KNOWN_HEADER = bidict(
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

KnownHeaderStr = Literal[
    "content_disposition",
    "content_type",
    "content_length",
    "location",
    "last_modified",
    "if_modified_since",
    "etag",
    "if_match",
    "if_none_match",
    "cookie",
    "set_cooke",
    "user_agent",
    "server",
]

PRIORITY = bidict(
    high=QtNetwork.QNetworkRequest.HighPriority,
    normal=QtNetwork.QNetworkRequest.NormalPriority,
    low=QtNetwork.QNetworkRequest.LowPriority,
)

PriorityStr = Literal["high", "normal", "low"]

REDIRECT_POLICIES = bidict(
    manual=QtNetwork.QNetworkRequest.ManualRedirectPolicy,
    no_less_safe=QtNetwork.QNetworkRequest.NoLessSafeRedirectPolicy,
    same_origin=QtNetwork.QNetworkRequest.SameOriginRedirectPolicy,
    user_verified=QtNetwork.QNetworkRequest.UserVerifiedRedirectPolicy,
)

RedirectPolicyStr = Literal["manual", "no_less_safe", "same_origin", "user_verified"]

CACHE_LOAD_CONTROL = bidict(
    always_network=QtNetwork.QNetworkRequest.AlwaysNetwork,
    prefer_network=QtNetwork.QNetworkRequest.PreferNetwork,
    prefer_cache=QtNetwork.QNetworkRequest.PreferCache,
    always_cache=QtNetwork.QNetworkRequest.AlwaysCache,
)

CacheLoadControlStr = Literal[
    "always_network", "prefer_network", "prefer_cache", "always_cache"
]


class NetworkRequest(QtNetwork.QNetworkRequest):
    def __init__(
        self, obj: Optional[Union[QtCore.QUrl, str, QtNetwork.QNetworkRequest]] = None
    ):
        if isinstance(obj, QtNetwork.QNetworkRequest):
            super().__init__(obj)
        else:
            super().__init__()
            if obj is not None:
                self.set_url(obj)

    def __repr__(self):
        return f"{type(self).__name__}({self.get_url()})"

    def set_header(self, name: KnownHeaderStr, value: str):
        if name not in KNOWN_HEADER:
            raise InvalidParamError(name, KNOWN_HEADER)
        self.setHeader(KNOWN_HEADER[name], value)

    def get_header(self, name: KnownHeaderStr) -> str:
        if name not in KNOWN_HEADER:
            raise InvalidParamError(name, KNOWN_HEADER)
        return self.header(KNOWN_HEADER[name])

    def set_headers(self, headers: Dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(k.encode(), v.encode())

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

    def set_priority(self, priority: PriorityStr):
        """Set priority.

        Args:
            priority: priority

        Raises:
            InvalidParamError: priority does not exist
        """
        if priority not in PRIORITY:
            raise InvalidParamError(priority, PRIORITY)
        self.setPriority(PRIORITY[priority])

    def get_priority(self) -> PriorityStr:
        """Get the current priority.

        Returns:
            priority
        """
        return PRIORITY.inverse[self.priority()]
