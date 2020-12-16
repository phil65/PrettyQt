# from qtpy import QtWebEngineWidgets
from typing import Literal

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


FONT_FAMILY = bidict(
    standard=QtWebEngineWidgets.QWebEngineSettings.StandardFont,
    fixed=QtWebEngineWidgets.QWebEngineSettings.FixedFont,
    serif=QtWebEngineWidgets.QWebEngineSettings.SerifFont,
    sans_serif=QtWebEngineWidgets.QWebEngineSettings.SansSerifFont,
    cursive=QtWebEngineWidgets.QWebEngineSettings.CursiveFont,
    fantasy=QtWebEngineWidgets.QWebEngineSettings.FantasyFont,
    pictograph=QtWebEngineWidgets.QWebEngineSettings.PictographFont,
)

FontFamilyStr = Literal[
    "standard", "fixed", "serif", "sans_serif", "cursive", "fantasy", "pictograph"
]

FONT_SIZE = bidict(
    minimum=QtWebEngineWidgets.QWebEngineSettings.MinimumFontSize,
    minimum_logical=QtWebEngineWidgets.QWebEngineSettings.MinimumLogicalFontSize,
    default=QtWebEngineWidgets.QWebEngineSettings.DefaultFontSize,
    default_fixed=QtWebEngineWidgets.QWebEngineSettings.DefaultFixedFontSize,
)

FontSizeStr = Literal["minimum", "minimum_logical", "default", "default_fixed"]

mod = QtWebEngineWidgets.QWebEngineSettings

UNKNOWN_URL_SCHEME_POLICY = bidict(
    disallow=mod.DisallowUnknownUrlSchemes,
    allow_from_user_interaction=mod.AllowUnknownUrlSchemesFromUserInteraction,
    allow_all=mod.AllowAllUnknownUrlSchemes,
)

UnknownUrlSchemePolicyStr = Literal[
    "disallow", "allow_from_user_interaction", "allow_all"
]

WEB_ATTRIBUTES = bidict(
    auto_load_images=mod.AutoLoadImages,
    javascript_enabled=mod.JavascriptEnabled,
    javascript_can_open_windows=mod.JavascriptCanOpenWindows,
    javascript_can_access_clipboard=mod.JavascriptCanAccessClipboard,
    links_included_in_focus_chain=mod.LinksIncludedInFocusChain,
    local_storage_enabled=mod.LocalStorageEnabled,
    local_content_can_access_remote_urls=mod.LocalContentCanAccessRemoteUrls,
    spatial_navigation_enabled=mod.SpatialNavigationEnabled,
    local_content_can_access_file_urls=mod.LocalContentCanAccessFileUrls,
    hyperlink_auditing_enabled=mod.HyperlinkAuditingEnabled,
    scroll_animator_enabled=mod.ScrollAnimatorEnabled,
    error_page_enabled=mod.ErrorPageEnabled,
    plugins_enabled=mod.PluginsEnabled,
    full_screen_support_enabled=mod.FullScreenSupportEnabled,
    screen_capture_enabled=mod.ScreenCaptureEnabled,
    web_gl_enabled=mod.WebGLEnabled,
    accelerated_2d_canvas_enabled=mod.Accelerated2dCanvasEnabled,
    auto_load_icons_for_page=mod.AutoLoadIconsForPage,
    touch_icons_enabled=mod.TouchIconsEnabled,
    focus_on_navigation_enabled=mod.FocusOnNavigationEnabled,
    print_element_backgrounds=mod.PrintElementBackgrounds,
    allow_running_insecure_content=mod.AllowRunningInsecureContent,
    allow_geolocation_on_insecure_origins=mod.AllowGeolocationOnInsecureOrigins,
    allow_window_activation_from_javascript=mod.AllowWindowActivationFromJavaScript,
    show_scrollbars=mod.ShowScrollBars,
    playback_requires_user_gesture=mod.PlaybackRequiresUserGesture,
    javascript_can_paste=mod.JavascriptCanPaste,
    web_rtc_public_interfaces_only=mod.WebRTCPublicInterfacesOnly,
    dns_prefetch_enabled=mod.DnsPrefetchEnabled,
)

if core.VersionNumber.get_qt_version() >= (5, 13, 0):
    WEB_ATTRIBUTES["pdf_viewer_enabled"] = mod.PdfViewerEnabled

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
    def __init__(self, item: QtWebEngineWidgets.QWebEngineSettings):
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
    from prettyqt import webenginewidgets, widgets

    app = widgets.app()
    page = webenginewidgets.WebEnginePage()
    settings = page.get_settings()
    app.main_loop()
