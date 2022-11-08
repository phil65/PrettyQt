# from prettyqt.qt import QtWebEngineCore
from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import InvalidParamError, bidict


FONT_FAMILY = bidict(
    standard=QtWebEngineCore.QWebEngineSettings.FontFamily.StandardFont,
    fixed=QtWebEngineCore.QWebEngineSettings.FontFamily.FixedFont,
    serif=QtWebEngineCore.QWebEngineSettings.FontFamily.SerifFont,
    sans_serif=QtWebEngineCore.QWebEngineSettings.FontFamily.SansSerifFont,
    cursive=QtWebEngineCore.QWebEngineSettings.FontFamily.CursiveFont,
    fantasy=QtWebEngineCore.QWebEngineSettings.FontFamily.FantasyFont,
    pictograph=QtWebEngineCore.QWebEngineSettings.FontFamily.PictographFont,
)

FontFamilyStr = Literal[
    "standard", "fixed", "serif", "sans_serif", "cursive", "fantasy", "pictograph"
]

FONT_SIZE = bidict(
    minimum=QtWebEngineCore.QWebEngineSettings.FontSize.MinimumFontSize,
    minimum_logical=QtWebEngineCore.QWebEngineSettings.FontSize.MinimumLogicalFontSize,
    default=QtWebEngineCore.QWebEngineSettings.FontSize.DefaultFontSize,
    default_fixed=QtWebEngineCore.QWebEngineSettings.FontSize.DefaultFixedFontSize,
)

FontSizeStr = Literal["minimum", "minimum_logical", "default", "default_fixed"]

mod = QtWebEngineCore.QWebEngineSettings

pol = mod.UnknownUrlSchemePolicy

UNKNOWN_URL_SCHEME_POLICY = bidict(
    disallow=pol.DisallowUnknownUrlSchemes,
    allow_from_user_interaction=pol.AllowUnknownUrlSchemesFromUserInteraction,
    allow_all=pol.AllowAllUnknownUrlSchemes,
)

UnknownUrlSchemePolicyStr = Literal[
    "disallow", "allow_from_user_interaction", "allow_all"
]

attr = mod.WebAttribute

WEB_ATTRIBUTES = bidict(
    auto_load_images=attr.AutoLoadImages,
    javascript_enabled=attr.JavascriptEnabled,
    javascript_can_open_windows=attr.JavascriptCanOpenWindows,
    javascript_can_access_clipboard=attr.JavascriptCanAccessClipboard,
    links_included_in_focus_chain=attr.LinksIncludedInFocusChain,
    local_storage_enabled=attr.LocalStorageEnabled,
    local_content_can_access_remote_urls=attr.LocalContentCanAccessRemoteUrls,
    spatial_navigation_enabled=attr.SpatialNavigationEnabled,
    local_content_can_access_file_urls=attr.LocalContentCanAccessFileUrls,
    hyperlink_auditing_enabled=attr.HyperlinkAuditingEnabled,
    scroll_animator_enabled=attr.ScrollAnimatorEnabled,
    error_page_enabled=attr.ErrorPageEnabled,
    plugins_enabled=attr.PluginsEnabled,
    full_screen_support_enabled=attr.FullScreenSupportEnabled,
    screen_capture_enabled=attr.ScreenCaptureEnabled,
    web_gl_enabled=attr.WebGLEnabled,
    accelerated_2d_canvas_enabled=attr.Accelerated2dCanvasEnabled,
    auto_load_icons_for_page=attr.AutoLoadIconsForPage,
    touch_icons_enabled=attr.TouchIconsEnabled,
    focus_on_navigation_enabled=attr.FocusOnNavigationEnabled,
    print_element_backgrounds=attr.PrintElementBackgrounds,
    allow_running_insecure_content=attr.AllowRunningInsecureContent,
    allow_geolocation_on_insecure_origins=attr.AllowGeolocationOnInsecureOrigins,
    allow_window_activation_from_javascript=attr.AllowWindowActivationFromJavaScript,
    show_scrollbars=attr.ShowScrollBars,
    playback_requires_user_gesture=attr.PlaybackRequiresUserGesture,
    javascript_can_paste=attr.JavascriptCanPaste,
    web_rtc_public_interfaces_only=attr.WebRTCPublicInterfacesOnly,
    dns_prefetch_enabled=attr.DnsPrefetchEnabled,
    pdf_viewer_enabled=mod.WebAttribute.PdfViewerEnabled,
)


WebAttributeStr = Literal[
    "auto_load_images",
    "javascript_enabled",
    "javascript_can_open_windows",
    "javascript_can_access_clipboard",
    "links_included_in_focus_chain",
    "local_storage_enabled",
    "local_content_can_access_remote_urls",
    "spatial_navigation_enabled",
    "local_content_can_access_file_urls",
    "hyperlink_auditing_enabled",
    "scroll_animator_enabled",
    "error_page_enabled",
    "plugins_enabled",
    "full_screen_support_enabled",
    "screen_capture_enabled",
    "web_gl_enabled",
    "accelerated_2d_canvas_enabled",
    "auto_load_icons_for_page",
    "touch_icons_enabled",
    "focus_on_navigation_enabled",
    "print_element_backgrounds",
    "allow_running_insecure_content",
    "allow_geolocation_on_insecure_origins",
    "allow_window_activation_from_javascript",
    "show_scrollbars",
    "playback_requires_user_gesture",
    "javascript_can_paste",
    "web_rtc_public_interfaces_only",
    "dns_prefetch_enabled",
    "pdf_viewer_enabled",
]


class WebEngineSettings:
    def __init__(self, item: QtWebEngineCore.QWebEngineSettings):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __setitem__(self, index: WebAttributeStr, value: bool):
        self.item.setAttribute(WEB_ATTRIBUTES[index], value)

    def __getitem__(self, index: WebAttributeStr) -> bool:
        return self.item.testAttribute(WEB_ATTRIBUTES[index])

    def __delitem__(self, index: WebAttributeStr):
        return self.item.resetAttribute(WEB_ATTRIBUTES[index])

    def set_unknown_url_scheme_policy(self, policy: UnknownUrlSchemePolicyStr):
        """Set the unknown url scheme policy.

        Args:
            policy: unknown url scheme policy

        Raises:
            InvalidParamError: Policy does not exist
        """
        if policy not in UNKNOWN_URL_SCHEME_POLICY:
            raise InvalidParamError(policy, UNKNOWN_URL_SCHEME_POLICY)
        self.item.setUnknownUrlSchemePolicy(UNKNOWN_URL_SCHEME_POLICY[policy])

    def get_unknown_url_scheme_policy(self) -> UnknownUrlSchemePolicyStr:
        """Return current unknown url scheme policy.

        Returns:
            Unknown url scheme policy
        """
        return UNKNOWN_URL_SCHEME_POLICY.inverse[self.item.unknownUrlSchemePolicy()]

    def set_font_family(self, which: FontFamilyStr, family: str):
        """Set the actual font family to family for the specified generic family, which.

        Args:
            which: family to set
            family: generic family

        Raises:
            InvalidParamError: Font family does not exist
        """
        if which not in FONT_FAMILY:
            raise InvalidParamError(which, FONT_FAMILY)
        self.item.setFontFamily(FONT_FAMILY[which], family)

    def get_font_family(self, family: FontFamilyStr) -> str:
        """Return the actual font family for the specified generic font family.

        Args:
            family: generic font family

        Returns:
            Font family
        """
        return self.item.fontFamily(FONT_FAMILY[family])

    def set_font_size(self, typ: FontSizeStr, size: int):
        """Set the font size for type to size in pixels.

        Args:
            typ: font size type
            size: size in pixels

        Raises:
            InvalidParamError: Font size does not exist
        """
        if typ not in FONT_SIZE:
            raise InvalidParamError(typ, FONT_SIZE)
        self.item.setFontSize(FONT_SIZE[typ], size)

    def get_font_size(self, typ: FontSizeStr) -> int:
        """Return the default font size for type in pixels.

        Args:
            typ: font size type

        Returns:
            Font size
        """
        return self.item.fontSize(FONT_SIZE[typ])


if __name__ == "__main__":
    from prettyqt import webenginecore, widgets

    app = widgets.app()
    page = webenginecore.WebEnginePage()
    settings = page.get_settings()
    app.main_loop()
