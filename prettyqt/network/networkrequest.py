from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypedDict

from prettyqt import core
from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict, datatypes, get_repr


Req = QtNetwork.QNetworkRequest
CE = Req.Attribute.ConnectionCacheExpiryTimeoutSecondsAttribute

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
    "connection_cache_expiry_timeout_seconds",
    "http2_cleartext_allowed",
    "use_credentials",
    "user",
    "user_max",
]

ATTRIBUTE: bidict[AttributeStr, Req.Attribute] = bidict(
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
    connection_cache_expiry_timeout_seconds=CE,
    http2_cleartext_allowed=Req.Attribute.Http2CleartextAllowedAttribute,
    use_credentials=Req.Attribute.UseCredentialsAttribute,
    user=Req.Attribute.User,
    user_max=Req.Attribute.UserMax,
)


class TypedAttribute(TypedDict):
    http_status_code: int
    http_reason_phrase: bytes
    redirection_target: core.QUrl
    connection_encrypted: bool
    cache_load_control: int
    cache_save_control: bool
    source_is_from_cache: bool
    do_not_buffer_upload_data: bool
    http_pipelining_allowed: bool
    http_pipelining_was_used: bool
    custom_verb: bytes
    cookie_load_control: int
    cookie_save_control: int
    authentication_reuse: int
    background_request: bool
    http2_allowed: bool
    http2_was_used: bool
    emit_all_upload_progress_signals: bool
    original_content_length: int
    redirect_policy: int
    http2_direct: bool
    auto_delete_reply_on_finish: bool
    user: Any
    user_max: Any


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

KNOWN_HEADER: bidict[KnownHeaderStr, Req.KnownHeaders] = bidict(
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

PriorityStr = Literal["high", "normal", "low"]

PRIORITY: bidict[PriorityStr, Req.Priority] = bidict(
    high=Req.Priority.HighPriority,
    normal=Req.Priority.NormalPriority,
    low=Req.Priority.LowPriority,
)

RedirectPolicyStr = Literal["manual", "no_less_safe", "same_origin", "user_verified"]

REDIRECT_POLICIES: bidict[RedirectPolicyStr, Req.RedirectPolicy] = bidict(
    manual=Req.RedirectPolicy.ManualRedirectPolicy,
    no_less_safe=Req.RedirectPolicy.NoLessSafeRedirectPolicy,
    same_origin=Req.RedirectPolicy.SameOriginRedirectPolicy,
    user_verified=Req.RedirectPolicy.UserVerifiedRedirectPolicy,
)

CacheLoadControlStr = Literal[
    "always_network", "prefer_network", "prefer_cache", "always_cache"
]

CACHE_LOAD_CONTROL: bidict[CacheLoadControlStr, Req.CacheLoadControl] = bidict(
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


class NetworkRequest(QtNetwork.QNetworkRequest):
    def __init__(self, obj: datatypes.UrlType | QtNetwork.QNetworkRequest | None = None):
        if isinstance(obj, QtNetwork.QNetworkRequest):
            super().__init__(obj)
        else:
            super().__init__()
            if obj is not None:
                self.set_url(obj)

    def __repr__(self):
        return get_repr(self, self.get_url())

    def set_header(self, name: KnownHeaderStr | Req.KnownHeaders, value: str):
        self.setHeader(KNOWN_HEADER.get_enum_value(name), value)

    def get_header(self, name: KnownHeaderStr | Req.KnownHeaders) -> str:
        return self.header(KNOWN_HEADER.get_enum_value(name))

    def set_headers(self, headers: Mapping[str, str]):
        for k, v in headers.items():
            self.setRawHeader(core.QByteArray(k.encode()), core.QByteArray(v.encode()))

    def get_headers(self) -> Mapping[str, str]:
        return {
            h.data().decode(): self.rawHeader(h).data().decode()
            for h in self.rawHeaderList()
        }

    def set_url(self, url: str | core.QUrl):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def set_priority(self, priority: PriorityStr | Req.Priority):
        """Set priority.

        Args:
            priority: priority
        """
        self.setPriority(PRIORITY.get_enum_value(priority))

    def get_priority(self) -> PriorityStr:
        """Get the current priority.

        Returns:
            priority
        """
        return PRIORITY.inverse[self.priority()]

    def set_attribute(
        self, attribute: AttributeStr | Req.Attribute, value: datatypes.Variant
    ):
        self.setAttribute(ATTRIBUTE.get_enum_value(attribute), value)

    def set_attributes(self, **kwargs):
        for k, v in kwargs.items():
            self.set_attribute(k, v)
