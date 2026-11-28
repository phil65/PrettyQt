from typing import TYPE_CHECKING, Literal, Self

from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict, get_repr


if TYPE_CHECKING:
    from collections.abc import Mapping


mod = QtNetwork.QHttpHeaders
Header = mod.WellKnownHeader

WellKnownHeaderStr = Literal[
    "aim",
    "alpn",
    "accept",
    "accept_additions",
    "accept_ch",
    "accept_charset",
    "accept_datetime",
    "accept_encoding",
    "accept_features",
    "accept_language",
    "accept_patch",
    "accept_post",
    "accept_ranges",
    "accept_signature",
    "access_control_allow_credentials",
    "access_control_allow_headers",
    "access_control_allow_methods",
    "access_control_allow_origin",
    "access_control_expose_headers",
    "access_control_max_age",
    "access_control_request_headers",
    "access_control_request_method",
    "age",
    "allow",
    "alt_svc",
    "alt_used",
    "alternates",
    "apply_to_redirect_ref",
    "authentication_control",
    "authentication_info",
    "authorization",
    "cdn_cache_control",
    "cdn_loop",
    "cpep_info",
    "cache_control",
    "cache_status",
    "cal_dav_timezones",
    "cal_managed_id",
    "capsule_protocol",
    "cert_not_after",
    "cert_not_before",
    "clear_site_data",
    "client_cert",
    "client_cert_chain",
    "close",
    "connection",
    "content_digest",
    "content_disposition",
    "content_encoding",
    "content_id",
    "content_language",
    "content_length",
    "content_location",
    "content_range",
    "content_security_policy",
    "content_security_policy_report_only",
    "content_type",
    "cookie",
    "cross_origin_embedder_policy",
    "cross_origin_embedder_policy_report_only",
    "cross_origin_opener_policy",
    "cross_origin_opener_policy_report_only",
    "cross_origin_resource_policy",
    "dasl",
    "dav",
    "dpop",
    "dpop_nonce",
    "date",
    "delta_base",
    "depth",
    "destination",
    "differential_id",
    "etag",
    "early_data",
    "expect",
    "expect_ct",
    "expires",
    "forwarded",
    "from",
    "hobareg",
    "host",
    "im",
    "if",
    "if_match",
    "if_modified_since",
    "if_none_match",
    "if_range",
    "if_schedule_tag_match",
    "if_unmodified_since",
    "include_referred_token_binding_id",
    "keep_alive",
    "label",
    "last_event_id",
    "last_modified",
    "link",
    "location",
    "lock_token",
    "mime_version",
    "max_forwards",
    "memento_datetime",
    "meter",
    "nel",
    "negotiate",
    "odata_entity_id",
    "odata_isolation",
    "odata_max_version",
    "odata_version",
    "oscore",
    "oslc_core_version",
    "optional_www_authenticate",
    "ordering_type",
    "origin",
    "origin_agent_cluster",
    "overwrite",
    "ping_from",
    "ping_to",
    "position",
    "pragma",
    "prefer",
    "preference_applied",
    "priority",
    "protocol_info",
    "protocol_query",
    "proxy_authenticate",
    "proxy_authentication_info",
    "proxy_authorization",
    "proxy_status",
    "public_key_pins",
    "public_key_pins_report_only",
    "range",
    "redirect_ref",
    "referer",
    "refresh",
    "replay_nonce",
    "repr_digest",
    "retry_after",
    "slug",
    "schedule_reply",
    "schedule_tag",
    "sec_purpose",
    "sec_token_binding",
    "sec_web_socket_accept",
    "sec_web_socket_extensions",
    "sec_web_socket_key",
    "sec_web_socket_protocol",
    "sec_web_socket_version",
    "server",
    "server_timing",
    "set_cookie",
    "signature",
    "signature_input",
    "soap_action",
    "status_uri",
    "strict_transport_security",
    "sunset",
    "surrogate_capability",
    "surrogate_control",
    "tcn",
    "te",
    "ttl",
    "timeout",
    "topic",
    "traceparent",
    "tracestate",
    "trailer",
    "transfer_encoding",
    "upgrade",
    "urgency",
    "user_agent",
    "variant_vary",
    "vary",
    "via",
    "www_authenticate",
    "want_content_digest",
    "want_repr_digest",
    "x_content_type_options",
    "x_frame_options",
]

WELL_KNOWN_HEADER: bidict[WellKnownHeaderStr, mod.WellKnownHeader] = bidict({
    "aim": Header.AIM,
    "alpn": Header.ALPN,
    "accept": Header.Accept,
    "accept_additions": Header.AcceptAdditions,
    "accept_ch": Header.AcceptCH,
    "accept_charset": Header.AcceptCharset,
    "accept_datetime": Header.AcceptDatetime,
    "accept_encoding": Header.AcceptEncoding,
    "accept_features": Header.AcceptFeatures,
    "accept_language": Header.AcceptLanguage,
    "accept_patch": Header.AcceptPatch,
    "accept_post": Header.AcceptPost,
    "accept_ranges": Header.AcceptRanges,
    "accept_signature": Header.AcceptSignature,
    "access_control_allow_credentials": Header.AccessControlAllowCredentials,
    "access_control_allow_headers": Header.AccessControlAllowHeaders,
    "access_control_allow_methods": Header.AccessControlAllowMethods,
    "access_control_allow_origin": Header.AccessControlAllowOrigin,
    "access_control_expose_headers": Header.AccessControlExposeHeaders,
    "access_control_max_age": Header.AccessControlMaxAge,
    "access_control_request_headers": Header.AccessControlRequestHeaders,
    "access_control_request_method": Header.AccessControlRequestMethod,
    "age": Header.Age,
    "allow": Header.Allow,
    "alt_svc": Header.AltSvc,
    "alt_used": Header.AltUsed,
    "alternates": Header.Alternates,
    "apply_to_redirect_ref": Header.ApplyToRedirectRef,
    "authentication_control": Header.AuthenticationControl,
    "authentication_info": Header.AuthenticationInfo,
    "authorization": Header.Authorization,
    "cdn_cache_control": Header.CDNCacheControl,
    "cdn_loop": Header.CDNLoop,
    "cpep_info": Header.CPEPInfo,
    "cache_control": Header.CacheControl,
    "cache_status": Header.CacheStatus,
    "cal_dav_timezones": Header.CalDAVTimezones,
    "cal_managed_id": Header.CalManagedID,
    "capsule_protocol": Header.CapsuleProtocol,
    "cert_not_after": Header.CertNotAfter,
    "cert_not_before": Header.CertNotBefore,
    "clear_site_data": Header.ClearSiteData,
    "client_cert": Header.ClientCert,
    "client_cert_chain": Header.ClientCertChain,
    "close": Header.Close,
    "connection": Header.Connection,
    "content_digest": Header.ContentDigest,
    "content_disposition": Header.ContentDisposition,
    "content_encoding": Header.ContentEncoding,
    "content_id": Header.ContentID,
    "content_language": Header.ContentLanguage,
    "content_length": Header.ContentLength,
    "content_location": Header.ContentLocation,
    "content_range": Header.ContentRange,
    "content_security_policy": Header.ContentSecurityPolicy,
    "content_security_policy_report_only": Header.ContentSecurityPolicyReportOnly,
    "content_type": Header.ContentType,
    "cookie": Header.Cookie,
    "cross_origin_embedder_policy": Header.CrossOriginEmbedderPolicy,
    "cross_origin_embedder_policy_report_only": (
        Header.CrossOriginEmbedderPolicyReportOnly
    ),
    "cross_origin_opener_policy": Header.CrossOriginOpenerPolicy,
    "cross_origin_opener_policy_report_only": Header.CrossOriginOpenerPolicyReportOnly,
    "cross_origin_resource_policy": Header.CrossOriginResourcePolicy,
    "dasl": Header.DASL,
    "dav": Header.DAV,
    "dpop": Header.DPoP,
    "dpop_nonce": Header.DPoPNonce,
    "date": Header.Date,
    "delta_base": Header.DeltaBase,
    "depth": Header.Depth,
    "destination": Header.Destination,
    "differential_id": Header.DifferentialID,
    "etag": Header.ETag,
    "early_data": Header.EarlyData,
    "expect": Header.Expect,
    "expect_ct": Header.ExpectCT,
    "expires": Header.Expires,
    "forwarded": Header.Forwarded,
    "from": Header.From,
    "hobareg": Header.Hobareg,
    "host": Header.Host,
    "im": Header.IM,
    "if": Header.If,
    "if_match": Header.IfMatch,
    "if_modified_since": Header.IfModifiedSince,
    "if_none_match": Header.IfNoneMatch,
    "if_range": Header.IfRange,
    "if_schedule_tag_match": Header.IfScheduleTagMatch,
    "if_unmodified_since": Header.IfUnmodifiedSince,
    "include_referred_token_binding_id": Header.IncludeReferredTokenBindingID,
    "keep_alive": Header.KeepAlive,
    "label": Header.Label,
    "last_event_id": Header.LastEventID,
    "last_modified": Header.LastModified,
    "link": Header.Link,
    "location": Header.Location,
    "lock_token": Header.LockToken,
    "mime_version": Header.MIMEVersion,
    "max_forwards": Header.MaxForwards,
    "memento_datetime": Header.MementoDatetime,
    "meter": Header.Meter,
    "nel": Header.NEL,
    "negotiate": Header.Negotiate,
    "odata_entity_id": Header.ODataEntityId,
    "odata_isolation": Header.ODataIsolation,
    "odata_max_version": Header.ODataMaxVersion,
    "odata_version": Header.ODataVersion,
    "oscore": Header.OSCORE,
    "oslc_core_version": Header.OSLCCoreVersion,
    "optional_www_authenticate": Header.OptionalWWWAuthenticate,
    "ordering_type": Header.OrderingType,
    "origin": Header.Origin,
    "origin_agent_cluster": Header.OriginAgentCluster,
    "overwrite": Header.Overwrite,
    "ping_from": Header.PingFrom,
    "ping_to": Header.PingTo,
    "position": Header.Position,
    "pragma": Header.Pragma,
    "prefer": Header.Prefer,
    "preference_applied": Header.PreferenceApplied,
    "priority": Header.Priority,
    "protocol_info": Header.ProtocolInfo,
    "protocol_query": Header.ProtocolQuery,
    "proxy_authenticate": Header.ProxyAuthenticate,
    "proxy_authentication_info": Header.ProxyAuthenticationInfo,
    "proxy_authorization": Header.ProxyAuthorization,
    "proxy_status": Header.ProxyStatus,
    "public_key_pins": Header.PublicKeyPins,
    "public_key_pins_report_only": Header.PublicKeyPinsReportOnly,
    "range": Header.Range,
    "redirect_ref": Header.RedirectRef,
    "referer": Header.Referer,
    "refresh": Header.Refresh,
    "replay_nonce": Header.ReplayNonce,
    "repr_digest": Header.ReprDigest,
    "retry_after": Header.RetryAfter,
    "slug": Header.SLUG,
    "schedule_reply": Header.ScheduleReply,
    "schedule_tag": Header.ScheduleTag,
    "sec_purpose": Header.SecPurpose,
    "sec_token_binding": Header.SecTokenBinding,
    "sec_web_socket_accept": Header.SecWebSocketAccept,
    "sec_web_socket_extensions": Header.SecWebSocketExtensions,
    "sec_web_socket_key": Header.SecWebSocketKey,
    "sec_web_socket_protocol": Header.SecWebSocketProtocol,
    "sec_web_socket_version": Header.SecWebSocketVersion,
    "server": Header.Server,
    "server_timing": Header.ServerTiming,
    "set_cookie": Header.SetCookie,
    "signature": Header.Signature,
    "signature_input": Header.SignatureInput,
    "soap_action": Header.SoapAction,
    "status_uri": Header.StatusURI,
    "strict_transport_security": Header.StrictTransportSecurity,
    "sunset": Header.Sunset,
    "surrogate_capability": Header.SurrogateCapability,
    "surrogate_control": Header.SurrogateControl,
    "tcn": Header.TCN,
    "te": Header.TE,
    "ttl": Header.TTL,
    "timeout": Header.Timeout,
    "topic": Header.Topic,
    "traceparent": Header.Traceparent,
    "tracestate": Header.Tracestate,
    "trailer": Header.Trailer,
    "transfer_encoding": Header.TransferEncoding,
    "upgrade": Header.Upgrade,
    "urgency": Header.Urgency,
    "user_agent": Header.UserAgent,
    "variant_vary": Header.VariantVary,
    "vary": Header.Vary,
    "via": Header.Via,
    "www_authenticate": Header.WWWAuthenticate,
    "want_content_digest": Header.WantContentDigest,
    "want_repr_digest": Header.WantReprDigest,
    "x_content_type_options": Header.XContentTypeOptions,
    "x_frame_options": Header.XFrameOptions,
})

HeaderNameType = WellKnownHeaderStr | mod.WellKnownHeader | str


def _resolve_name(name: HeaderNameType) -> mod.WellKnownHeader | str:
    if isinstance(name, str) and name in WELL_KNOWN_HEADER:
        return WELL_KNOWN_HEADER[name]
    return name


class HttpHeaders(QtNetwork.QHttpHeaders):
    """Holds HTTP headers for network requests and replies."""

    def __repr__(self):
        return get_repr(self, self.to_dict())

    def __len__(self) -> int:
        return self.size()

    def __bool__(self) -> bool:
        return not self.isEmpty()

    def __contains__(self, name: HeaderNameType) -> bool:
        return self.contains(_resolve_name(name))

    def __getitem__(self, name: HeaderNameType) -> str:
        if name not in self:
            raise KeyError(name)
        return self.get_value(name)

    def __setitem__(self, name: HeaderNameType, value: str):
        self.replace_or_append(name, value)

    def __delitem__(self, name: HeaderNameType):
        if name not in self:
            raise KeyError(name)
        self.remove_all(name)

    def append_header(self, name: HeaderNameType, value: str) -> bool:
        """Append a header entry with the given name and value."""
        return self.append(_resolve_name(name), value)

    def replace_or_append(self, name: HeaderNameType, value: str) -> bool:
        """Replace the first occurrence of name or append if not present."""
        return self.replaceOrAppend(_resolve_name(name), value)

    def remove_all(self, name: HeaderNameType):
        """Remove all header entries with the given name."""
        self.removeAll(_resolve_name(name))

    def get_value(self, name: HeaderNameType, default: str = "") -> str:
        """Return the first value for the given header name, or default if absent."""
        vals = self.values(_resolve_name(name))
        if not vals:
            return default
        return bytes(vals[0].data()).decode()

    def get_values(self, name: HeaderNameType) -> list[str]:
        """Return all values for the given header name."""
        return [bytes(v.data()).decode() for v in self.values(_resolve_name(name))]

    def get_combined_value(self, name: HeaderNameType) -> str:
        """Return all values for the given header name combined with commas."""
        return bytes(self.combinedValue(_resolve_name(name)).data()).decode()

    def to_list(self) -> list[tuple[str, str]]:
        """Return all headers as a list of (name, value) string pairs."""
        return [
            (bytes(k.data()).decode(), bytes(v.data()).decode())
            for k, v in self.toListOfPairs()
        ]

    def to_dict(self) -> dict[str, str]:
        """Return all headers as a dict mapping header names to values."""
        return dict(self.to_list())

    @classmethod
    def from_dict(cls, headers: Mapping[str, str]) -> Self:
        """Create an HttpHeaders instance from a mapping of header names to values."""
        instance = cls()
        for k, v in headers.items():
            instance.append_header(k, v)
        return instance


if __name__ == "__main__":
    headers = HttpHeaders.from_dict({"content_type": "application/json"})
    print(repr(headers))
