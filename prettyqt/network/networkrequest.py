from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import InvalidParamError, bidict


Req = QtNetwork.QNetworkRequest

ATTRIBUTE = bidict(
    http_status_code=Req.HttpStatusCodeAttribute,
    http_reason_phrase=Req.HttpReasonPhraseAttribute,
    redirection_target=Req.RedirectionTargetAttribute,
    connection_encrypted=Req.ConnectionEncryptedAttribute,
    cache_load_control=Req.CacheLoadControlAttribute,
    cache_save_control=Req.CacheSaveControlAttribute,
    source_is_from_cache=Req.SourceIsFromCacheAttribute,
    do_not_buffer_upload_data=Req.DoNotBufferUploadDataAttribute,
    http_pipelining_allowed=Req.HttpPipeliningAllowedAttribute,
    http_pipelining_was_used=Req.HttpPipeliningWasUsedAttribute,
    custom_verb=Req.CustomVerbAttribute,
    cookie_load_control=Req.CookieLoadControlAttribute,
    cookie_save_control=Req.CookieSaveControlAttribute,
    authentication_reuse=Req.AuthenticationReuseAttribute,
    background_request=Req.BackgroundRequestAttribute,
    http2_allowed=Req.Http2AllowedAttribute,
    http2_was_used=Req.Http2WasUsedAttribute,
    emit_all_upload_progress_signals=Req.EmitAllUploadProgressSignalsAttribute,
    original_content_length=Req.OriginalContentLengthAttribute,
    redirect_policy=Req.RedirectPolicyAttribute,
    http2_direct=Req.Http2DirectAttribute,
    auto_delete_reply_on_finish=Req.AutoDeleteReplyOnFinishAttribute,
    user=Req.User,
    user_max=Req.UserMax,
)

AttributeStr = Literal[
    "http_status_code",
    "http_reason_phrase",
    "redirection_target",
    "connection_encrypted",
    "cache_load_control",
    "cache_save_control",
    "source_is_from_cache",
    "do_not_buffer_upload_data",
    "http_pipelining_allowed",
    "http_pipelining_was_used",
    "custom_verb",
    "cookie_load_control",
    "cookie_save_control",
    "authentication_reuse",
    "background_request",
    "http2_allowed",
    "http2_was_used",
    "emit_all_upload_progress_signals",
    "original_content_length",
    "redirect_policy",
    "http2_direct",
    "auto_delete_reply_on_finish",
    "user",
    "user_max",
]

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
    def __init__(self, obj: QtCore.QUrl | str | QtNetwork.QNetworkRequest | None = None):
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

    def set_headers(self, headers: dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(
                QtCore.QByteArray(k.encode()), QtCore.QByteArray(v.encode())
            )

    def get_headers(self) -> dict[str, str]:
        return {
            bytes(h).decode(): bytes(self.rawHeader(h)).decode()
            for h in self.rawHeaderList()
        }

    def set_url(self, url: str | QtCore.QUrl):
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
