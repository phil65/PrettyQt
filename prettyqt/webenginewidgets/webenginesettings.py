# -*- coding: utf-8 -*-

# from qtpy import QtWebEngineWidgets

from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


FONT_FAMILIES = bidict(
    standard=QtWebEngineWidgets.QWebEngineSettings.StandardFont,
    fixed=QtWebEngineWidgets.QWebEngineSettings.FixedFont,
    serif=QtWebEngineWidgets.QWebEngineSettings.SerifFont,
    sans_serif=QtWebEngineWidgets.QWebEngineSettings.SansSerifFont,
    cursive=QtWebEngineWidgets.QWebEngineSettings.CursiveFont,
    fantasy=QtWebEngineWidgets.QWebEngineSettings.FantasyFont,
    pictograph=QtWebEngineWidgets.QWebEngineSettings.PictographFont,
)

FONT_SIZES = bidict(
    minimum=QtWebEngineWidgets.QWebEngineSettings.MinimumFontSize,
    minimum_logical=QtWebEngineWidgets.QWebEngineSettings.MinimumLogicalFontSize,
    default=QtWebEngineWidgets.QWebEngineSettings.DefaultFontSize,
    default_fixed=QtWebEngineWidgets.QWebEngineSettings.DefaultFixedFontSize,
)

mod = QtWebEngineWidgets.QWebEngineSettings

UNKNOWN_URL_SCHEME_POLICY = bidict(
    disallow=mod.DisallowUnknownUrlSchemes,
    allow_from_user_interaction=mod.AllowUnknownUrlSchemesFromUserInteraction,
    allow_all=mod.AllowAllUnknownUrlSchemes,
)

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


class WebEngineSettings:
    def __init__(self, item: QtWebEngineWidgets.QWebEngineSettings):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __setitem__(self, index: str, value: bool):
        self.item.setAttribute(WEB_ATTRIBUTES[index], value)

    def __getitem__(self, index: str) -> bool:
        return self.item.testAttribute(WEB_ATTRIBUTES[index])

    def set_unknown_url_scheme_policy(self, policy: str):
        """Set the unknown url scheme policy.

        Allowed values are "disallow", "allow_from_user_interaction", "allow_all"

        Args:
            policy: unknown url scheme policy

        Raises:
            InvalidParamError: Policy does not exist
        """
        if policy not in UNKNOWN_URL_SCHEME_POLICY:
            raise InvalidParamError(policy, UNKNOWN_URL_SCHEME_POLICY)
        self.item.setUnknownUrlSchemePolicy(UNKNOWN_URL_SCHEME_POLICY[policy])

    def get_unknown_url_scheme_policy(self) -> str:
        """Return current unknown url scheme policy.

        Possible values are "disallow", "allow_from_user_interaction", "allow_all"

        Returns:
            Unknown url scheme policy
        """
        return UNKNOWN_URL_SCHEME_POLICY.inv[self.item.unknownUrlSchemePolicy()]

    def set_font_family(self, which: str, family: str):
        """Set the actual font family to family for the specified generic family, which.

        Args:
            which: family to set
            family: generic family

        Raises:
            InvalidParamError: Font family does not exist
        """
        if which not in FONT_FAMILIES:
            raise InvalidParamError(which, FONT_FAMILIES)
        self.item.setFontFamily(FONT_FAMILIES[which], family)

    def get_font_family(self, family: str) -> str:
        """Return the actual font family for the specified generic font family.

        Possible values are "standard", "fixed", "serif", "sans_serif", "cursive",
                            "fantasy", "pictograph"

        Args:
            family: generic font family

        Returns:
            Font family
        """
        return self.item.fontFamily(FONT_FAMILIES[family])

    def set_font_size(self, typ: str, size: int):
        """Set the font size for type to size in pixels.

        Args:
            typ: font size type
            size: size in pixels

        Raises:
            InvalidParamError: Font size does not exist
        """
        if typ not in FONT_SIZES:
            raise InvalidParamError(typ, FONT_SIZES)
        self.item.setFontSize(FONT_SIZES[typ], size)

    def get_font_size(self, typ: str) -> int:
        """Return the default font size for type in pixels.

        Possible values are "minimum", "minimum_logical", "default", "default_fixed"

        Args:
            typ: font size type

        Returns:
            Font size
        """
        return self.item.fontSize(FONT_SIZES[typ])


if __name__ == "__main__":
    from prettyqt import widgets, webenginewidgets

    app = widgets.app()
    page = webenginewidgets.WebEnginePage()
    settings = page.get_settings()
    app.main_loop()
