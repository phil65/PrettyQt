from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Literal
import webbrowser

from prettyqt import core, gui, webenginecore
from prettyqt.utils import bidict, datatypes


if TYPE_CHECKING:
    from collections.abc import Callable


mod = webenginecore.QWebEnginePage

logger = logging.getLogger(__name__)


FeatureStr = Literal[
    "notifications",
    "geolocation",
    "media_audio_capture",
    "media_video_capture",
    "media_audiovideo_capture",
    "mouse_lock",
    "desktop_video_capture",
    "desktop_audiovideo_capture",
]

FEATURE: bidict[FeatureStr, mod.Feature] = bidict(
    notifications=mod.Feature.Notifications,
    geolocation=mod.Feature.Geolocation,
    media_audio_capture=mod.Feature.MediaAudioCapture,
    media_video_capture=mod.Feature.MediaVideoCapture,
    media_audiovideo_capture=mod.Feature.MediaAudioVideoCapture,
    mouse_lock=mod.Feature.MouseLock,
    desktop_video_capture=mod.Feature.DesktopVideoCapture,
    desktop_audiovideo_capture=mod.Feature.DesktopAudioVideoCapture,
)

FileSelectionModeStr = Literal["open", "open_multiple"]

FILE_SELECTION_MODE: bidict[FileSelectionModeStr, mod.FileSelectionMode] = bidict(
    open=mod.FileSelectionMode.FileSelectOpen,
    open_multiple=mod.FileSelectionMode.FileSelectOpenMultiple,
)

FindFlagStr = Literal["backward", "case_sensitive"]

FIND_FLAGS: bidict[FindFlagStr, mod.FindFlag] = bidict(
    backward=mod.FindFlag.FindBackward,
    case_sensitive=mod.FindFlag.FindCaseSensitively,
)

JavaScriptConsoleMessageLevelStr = Literal["info", "warning", "error"]

JS_CONSOLE_MESSAGE_LEVEL: bidict[
    JavaScriptConsoleMessageLevelStr, mod.JavaScriptConsoleMessageLevel
] = bidict(
    info=mod.JavaScriptConsoleMessageLevel.InfoMessageLevel,
    warning=mod.JavaScriptConsoleMessageLevel.WarningMessageLevel,
    error=mod.JavaScriptConsoleMessageLevel.ErrorMessageLevel,
)

LifecycleStateStr = Literal["active", "frozen", "discarded"]

LIFECYCLE_STATE: bidict[LifecycleStateStr, mod.LifecycleState] = bidict(
    active=mod.LifecycleState.Active,
    frozen=mod.LifecycleState.Frozen,
    discarded=mod.LifecycleState.Discarded,
)

NAVIGATION_TYPES = bidict(
    link_clicked=mod.NavigationType.NavigationTypeLinkClicked,
    typed=mod.NavigationType.NavigationTypeTyped,
    form_submitted=mod.NavigationType.NavigationTypeFormSubmitted,
    back_forward=mod.NavigationType.NavigationTypeBackForward,
    reload=mod.NavigationType.NavigationTypeReload,
    redirect=mod.NavigationType.NavigationTypeRedirect,
    other=mod.NavigationType.NavigationTypeOther,
)

PermissionPolicyStr = Literal["unknown", "granted_by_user", "denied_by_user"]

PERMISSION_POLICY: bidict[PermissionPolicyStr, mod.PermissionPolicy] = bidict(
    unknown=mod.PermissionPolicy.PermissionUnknown,
    granted_by_user=mod.PermissionPolicy.PermissionGrantedByUser,
    denied_by_user=mod.PermissionPolicy.PermissionDeniedByUser,
)

RENDER_PROCESS_TERMINATION_STATUS = bidict(
    normal=mod.RenderProcessTerminationStatus.NormalTerminationStatus,
    abnormal=mod.RenderProcessTerminationStatus.AbnormalTerminationStatus,
    crashed=mod.RenderProcessTerminationStatus.CrashedTerminationStatus,
    killed=mod.RenderProcessTerminationStatus.KilledTerminationStatus,
)

WebActionStr = Literal[
    "none",
    "back",
    "forward",
    "stop",
    "reload",
    "reload_and_bypass_cache",
    "cut",
    "copy",
    "paste",
    "undo",
    "redo",
    "select_all",
    "paste_and_match_style",
    "open_link_in_this_window",
    "open_link_in_new_window",
    "open_link_in_new_tab",
    "open_link_in_new_bg_tab",
    "copy_link_to_clipboard",
    "copy_image_to_clipboard",
    "copy_image_url_to_clipboard",
    "copy_media_url_to_clipboard",
    "toggle_media_controls",
    "toggle_media_loop",
    "toggle_media_play_pause",
    "toggle_media_mute",
    "download_link_to_disk",
    "download_image_to_disk",
    "download_media_to_disk",
    "inspect_element",
    "exit_fullscreen",
    "request_close",
    "unselect",
    "save_page",
    "view_source",
    "toggle_bold",
    "toggle_italic",
    "toggle_underline",
    "toggle_strikethrough",
    "align_left",
    "align_center",
    "align_right",
    "align_justified",
    "indent",
    "outdent",
    "insert_ordered_list",
    "insert_unordered_list",
]

WEB_ACTION: bidict[WebActionStr, mod.WebAction] = bidict(
    none=mod.WebAction.NoWebAction,
    back=mod.WebAction.Back,
    forward=mod.WebAction.Forward,
    stop=mod.WebAction.Stop,
    reload=mod.WebAction.Reload,
    reload_and_bypass_cache=mod.WebAction.ReloadAndBypassCache,
    cut=mod.WebAction.Cut,
    copy=mod.WebAction.Copy,
    paste=mod.WebAction.Paste,
    undo=mod.WebAction.Undo,
    redo=mod.WebAction.Redo,
    select_all=mod.WebAction.SelectAll,
    paste_and_match_style=mod.WebAction.PasteAndMatchStyle,
    open_link_in_this_window=mod.WebAction.OpenLinkInThisWindow,
    open_link_in_new_window=mod.WebAction.OpenLinkInNewWindow,
    open_link_in_new_tab=mod.WebAction.OpenLinkInNewTab,
    open_link_in_new_bg_tab=mod.WebAction.OpenLinkInNewBackgroundTab,
    copy_link_to_clipboard=mod.WebAction.CopyLinkToClipboard,
    copy_image_to_clipboard=mod.WebAction.CopyImageToClipboard,
    copy_image_url_to_clipboard=mod.WebAction.CopyImageUrlToClipboard,
    copy_media_url_to_clipboard=mod.WebAction.CopyMediaUrlToClipboard,
    toggle_media_controls=mod.WebAction.ToggleMediaControls,
    toggle_media_loop=mod.WebAction.ToggleMediaLoop,
    toggle_media_play_pause=mod.WebAction.ToggleMediaPlayPause,
    toggle_media_mute=mod.WebAction.ToggleMediaMute,
    download_link_to_disk=mod.WebAction.DownloadLinkToDisk,
    download_image_to_disk=mod.WebAction.DownloadImageToDisk,
    download_media_to_disk=mod.WebAction.DownloadMediaToDisk,
    inspect_element=mod.WebAction.InspectElement,
    exit_fullscreen=mod.WebAction.ExitFullScreen,
    request_close=mod.WebAction.RequestClose,
    unselect=mod.WebAction.Unselect,
    save_page=mod.WebAction.SavePage,
    view_source=mod.WebAction.ViewSource,
    toggle_bold=mod.WebAction.ToggleBold,
    toggle_italic=mod.WebAction.ToggleItalic,
    toggle_underline=mod.WebAction.ToggleUnderline,
    toggle_strikethrough=mod.WebAction.ToggleStrikethrough,
    align_left=mod.WebAction.AlignLeft,
    align_center=mod.WebAction.AlignCenter,
    align_right=mod.WebAction.AlignRight,
    align_justified=mod.WebAction.AlignJustified,
    indent=mod.WebAction.Indent,
    outdent=mod.WebAction.Outdent,
    insert_ordered_list=mod.WebAction.InsertOrderedList,
    insert_unordered_list=mod.WebAction.InsertUnorderedList,
)

WEB_WINDOW_TYPES = bidict(
    browser_window=mod.WebWindowType.WebBrowserWindow,
    browser_tab=mod.WebWindowType.WebBrowserTab,
    dialog=mod.WebWindowType.WebDialog,
    browser_bg_tab=mod.WebWindowType.WebBrowserBackgroundTab,
)


class WebEnginePage(core.ObjectMixin, webenginecore.QWebEnginePage):
    """A web engine page holds the HTML document contents, link history + actions."""

    def get_icon(self) -> gui.Icon | None:
        """Return icon. If icon is Null, return None."""
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def set_url(self, url: datatypes.PathType | datatypes.UrlType):
        """Set the url of the WebEnginePage.

        Clears the Page and loads the URL.

        Args:
            url: URL to set
        """
        self.setUrl(datatypes.to_url(url))

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def get_icon_url(self) -> core.Url:
        return core.Url(self.iconUrl())

    def get_requested_url(self) -> core.Url:
        return core.Url(self.requestedUrl())

    def get_scroll_position(self) -> core.PointF:
        return core.PointF(self.scrollPosition())

    def get_contents_size(self) -> core.SizeF:
        return core.SizeF(self.contentsSize())

    def load_url(self, url: datatypes.UrlType | datatypes.PathType):
        """Load the URL.

        Loads the specified url and displays it.

        Note: The Page remains the same until enough data has arrived
        to display the new URL.

        Args:
            url: URL to load
        """
        self.load(datatypes.to_url(url))

    def set_zoom(self, zoom: float):
        """Set the zoom factor for the Page.

        Valid values are within the range from 0.25 to 5.0. The default factor is 1.0.

        Args:
            zoom: Zoom factor
        """
        self.setZoomFactor(zoom)

    def find_text(
        self,
        string: str,
        backward: bool = False,
        case_sensitive: bool = False,
        callback: Callable[[bool], None] | None = None,
    ):
        """Find text in the current page.

        Finds the specified string, subString, in the page, using the given options.
        The findTextFinished() signal is emitted when a string search is completed.

        To clear the search highlight, just pass an empty string.

        The resultCallback must take a boolean parameter.
        It will be called with a value of true if the subString was found;
        otherwise the callback value will be false.

        Warning: It is guaranteed that the callback is always called,
        but it might be done during page destruction. When WebEnginePage is deleted,
        the callback is triggered with an invalid value and it is not safe to use
        the corresponding QWebEnginePage or QWebEnginePage instance inside it.

        Args:
            string: string to search for
            backward: search backwards
            case_sensitive: case-sensitive search
            callback: result callback
        """
        if callback is None:

            def do_nothing(x):
                pass

            callback = do_nothing
        flag = webenginecore.QWebEnginePage.FindFlag(0)
        if case_sensitive:
            flag |= self.FindFlag.FindCaseSensitively
        if backward:
            flag |= self.FindFlag.FindBackward
        self.findText(string, flag, callback)

    def set_lifecycle_state(self, state: LifecycleStateStr | mod.LifecycleState):
        """Set lifecycle state.

        Args:
            state: lifecycle state
        """
        self.setLifecycleState(LIFECYCLE_STATE.get_enum_value(state))

    def get_lifecycle_state(self) -> LifecycleStateStr:
        """Get the current lifecycle state.

        Returns:
            lifecycle state
        """
        return LIFECYCLE_STATE.inverse[self.lifecycleState()]

    def trigger_action(self, action: WebActionStr | mod.WebAction, checked: bool = False):
        """Trigger action."""
        self.triggerAction(WEB_ACTION.get_enum_value(action), checked)

    def set_feature_permission(
        self,
        url: datatypes.UrlType,
        feature: FeatureStr | mod.Feature,
        policy: PermissionPolicyStr | mod.PermissionPolicy,
    ):
        """Set permission of feature for given URL."""
        url = core.Url(url)
        self.setFeaturePermission(
            url, FEATURE.get_enum_value(feature), PERMISSION_POLICY.get_enum_value(policy)
        )

    def get_history(self) -> webenginecore.WebEngineHistory:
        hist = self.history()
        return webenginecore.WebEngineHistory(hist)

    def get_settings(self) -> webenginecore.WebEngineSettings:
        """Get WebEngineSettings (a MutableMapping)."""
        settings = self.settings()
        return webenginecore.WebEngineSettings(settings)

    def set_setting(
        self,
        setting_name: webenginecore.webenginesettings.WebAttributeStr,
        value: bool,
    ):
        """Set WebEngine setting to value."""
        self.get_settings()[setting_name] = value

    def get_setting(
        self,
        setting_name: webenginecore.webenginesettings.WebAttributeStr,
    ) -> bool:
        """Return value of given WebEngine setting."""
        return self.get_settings()[setting_name]

    def get_scripts(self) -> webenginecore.WebEngineScriptCollection:
        """Get script collection."""
        return webenginecore.WebEngineScriptCollection(self.scripts())

    def open_in_browser(self):
        """Open page URL in default system browser."""
        try:
            webbrowser.open(self.getUrl().toString())
        except ValueError:
            logger.exception("Error opening URL %r", self.getUrl().toString())

    def insert_stylesheet(
        self, name: str, css: str | os.PathLike[str], immediately: bool = True
    ):
        """Load css using JavaScript.

        Arguments:
            name: CSS id
            css: CSS stylesheet, either a string or a PathLike object.
            immediately: whther to run javascript immediately
        """
        if isinstance(css, os.PathLike):
            path = core.File(os.fspath(css))
            if not path.open(
                core.File.OpenModeFlag.ReadOnly | core.File.OpenModeFlag.Text
            ):
                return
            css = path.readAll().data().decode("utf-8")
        script = webenginecore.WebEngineScript()
        s = """
        (function() {
        css = document.createElement('style');
        css.type = 'text/css';
        css.id = "%s";
        document.head.appendChild(css);
        css.innerText = `%s`;
        })()
        """
        s = s % (name, css)
        script = webenginecore.WebEngineScript()
        if immediately:
            self.runJavaScript(s, script.ScriptWorldId.ApplicationWorld)
        script.setName(name)
        script.setSourceCode(s)
        script.setInjectionPoint(script.InjectionPoint.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(script.ScriptWorldId.ApplicationWorld)
        self.scripts().insert(script)

    def mousedown(self, selector: str, btn: Literal["left", "middle", "right"]):
        """Simulate a mousedown event on the targeted element.

        Arguments:
            selector: A CSS3 selector to targeted element
            btn: Mouse button
        """
        btn_id = dict(left=0, middle=1, right=2)[btn]
        return self.runJavaScript(
            f"""
            (function () {{
                var element = document.querySelector({selector!r});
                var evt = document.createEvent("MouseEvents");
                evt.initMouseEvent("mousedown", true, true, window,
                                   1, 1, 1, 1, 1, false, false, false, false,
                                   {btn_id!r}, element);
                return element.dispatchEvent(evt);
            }})();
        """
        )

    def set_input_value(self, selector: str, value):
        """Set the value of the input matched by given selector."""
        script = f'document.querySelector({selector!r}).setAttribute("value", "{value}")'
        self.runJavaScript(script)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    path = path = "E:\\dev\\datacook\\processanalyzer\\docs\\index.html"
    widget = WebEnginePage()
    widget.set_url(path)
    widget.find_text("test", backward=True, case_sensitive=True, callback=None)
    app.exec()
