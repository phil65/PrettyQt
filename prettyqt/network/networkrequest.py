from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import InvalidParamError, bidict, types


Req = QtNetwork.QNetworkRequest

ATTRIBUTE = bidict(
    http_status_code=Req.Attribute.HttpStatusCodeAttribute,
    http_reason_phrase=Req.Attribute.HttpReasonPhraseAttribute,
    redirection_target=Req.Attribute.RedirectionTargetAttribute,
    connection_encrypted=Req.Attribute.ConnectionEncryptedAttribute,
    cache_load_control=Req.Attribute.CacheLoadControlAttribute,
    cache_save_control=Req.Attribute.CacheSaveControlAttribute,
    source_is_from_cache=Req.Attribute.SourceIsFromCacheAttribute,
    do_not_buffer_upload_data=Req.Attribute.DoNotBufferUploadDataAttribute,
    http_pipelining_allowed=Req.Attribute.HttpPipeliningAllowedAttribute,
    http_pipelining_was_used=Req.Attribute.HttpPipeliningWasUsedAttribute,
    custom_verb=Req.Attribute.CustomVerbAttribute,
    cookie_load_control=Req.Attribute.CookieLoadControlAttribute,
    cookie_save_control=Req.Attribute.CookieSaveControlAttribute,
    authentication_reuse=Req.Attribute.AuthenticationReuseAttribute,
    background_request=Req.Attribute.BackgroundRequestAttribute,
    http2_allowed=Req.Attribute.Http2AllowedAttribute,
    http2_was_used=Req.Attribute.Http2WasUsedAttribute,
    emit_all_upload_progress_signals=Req.Attribute.EmitAllUploadProgressSignalsAttribute,
    original_content_length=Req.Attribute.OriginalContentLengthAttribute,
    redirect_policy=Req.Attribute.RedirectPolicyAttribute,
    http2_direct=Req.Attribute.Http2DirectAttribute,
    auto_delete_reply_on_finish=Req.Attribute.AutoDeleteReplyOnFinishAttribute,
    user=Req.Attribute.User,
    user_max=Req.Attribute.UserMax,
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
    content_disposition=Req.KnownHeaders.ContentDispositionHeader,
    content_type=Req.KnownHeaders.ContentTypeHeader,
    content_length=Req.KnownHeaders.ContentLengthHeader,
    location=Req.KnownHeaders.LocationHeader,
    last_modified=Req.KnownHeaders.LastModifiedHeader,
    if_modified_since=Req.KnownHeaders.IfModifiedSinceHeader,
    etag=Req.KnownHeaders.ETagHeader,
    if_match=Req.KnownHeaders.IfMatchHeader,
    if_none_match=Req.KnownHeaders.IfNoneMatchHeader,
    cookie=Req.KnownHeaders.CookieHeader,
    set_cooke=Req.KnownHeaders.SetCookieHeader,
    user_agent=Req.KnownHeaders.UserAgentHeader,
    server=Req.KnownHeaders.ServerHeader,
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
    high=Req.Priority.HighPriority,
    normal=Req.Priority.NormalPriority,
    low=Req.Priority.LowPriority,
)

PriorityStr = Literal["high", "normal", "low"]

REDIRECT_POLICIES = bidict(
    manual=Req.RedirectPolicy.ManualRedirectPolicy,
    no_less_safe=Req.RedirectPolicy.NoLessSafeRedirectPolicy,
    same_origin=Req.RedirectPolicy.SameOriginRedirectPolicy,
    user_verified=Req.RedirectPolicy.UserVerifiedRedirectPolicy,
)

RedirectPolicyStr = Literal["manual", "no_less_safe", "same_origin", "user_verified"]

# if core.VersionNumber.get_qt_version() >= (6, 2, 0):
CACHE_LOAD_CONTROL = bidict(
    always_network=Req.CacheLoadControl.AlwaysNetwork,
    prefer_network=Req.CacheLoadControl.PreferNetwork,
    prefer_cache=Req.CacheLoadControl.PreferCache,
    always_cache=Req.CacheLoadControl.AlwaysCache,
)
# else:
#     CACHE_LOAD_CONTROL = bidict(
#         always_network=Req.CacheLoadControlAlwaysNetwork,
#         prefer_network=Req.CacheLoadControlPreferNetwork,
#         prefer_cache=Req.CacheLoadControlPreferCache,
#         always_cache=Req.CacheLoadControlAlwaysCache,
# )
CacheLoadControlStr = Literal[
    "always_network", "prefer_network", "prefer_cache", "always_cache"
]


class NetworkRequest(QtNetwork.QNetworkRequest):
    def __init__(self, obj: types.UrlType | QtNetwork.QNetworkRequest | None = None):
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
