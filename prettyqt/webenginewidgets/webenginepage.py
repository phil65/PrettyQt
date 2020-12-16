import pathlib
from typing import Callable, Literal, Union

from qtpy import QtCore, QtWebEngineWidgets

from prettyqt import core, gui, webenginewidgets
from prettyqt.utils import InvalidParamError, bidict


QtWebEngineWidgets.QWebEnginePage.__bases__ = (core.Object,)


FEATURE = bidict(
    notifications=QtWebEngineWidgets.QWebEnginePage.Notifications,
    geolocation=QtWebEngineWidgets.QWebEnginePage.Geolocation,
    media_audio_capture=QtWebEngineWidgets.QWebEnginePage.MediaAudioCapture,
    media_video_capture=QtWebEngineWidgets.QWebEnginePage.MediaVideoCapture,
    media_audiovideo_capture=QtWebEngineWidgets.QWebEnginePage.MediaAudioVideoCapture,
    mouse_lock=QtWebEngineWidgets.QWebEnginePage.MouseLock,
    desktop_video_capture=QtWebEngineWidgets.QWebEnginePage.DesktopVideoCapture,
    desktop_audiovideo_capture=QtWebEngineWidgets.QWebEnginePage.DesktopAudioVideoCapture,
)

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

FILE_SELECTION_MODE = bidict(
    open=QtWebEngineWidgets.QWebEnginePage.FileSelectOpen,
    open_multiple=QtWebEngineWidgets.QWebEnginePage.FileSelectOpenMultiple,
)

FileSelectionModeStr = Literal["open", "open_multiple"]

FIND_FLAGS = bidict(
    backward=QtWebEngineWidgets.QWebEnginePage.FindBackward,
    case_sensitive=QtWebEngineWidgets.QWebEnginePage.FindCaseSensitively,
)

FindFlagStr = Literal["backward", "case_sensitive"]

JS_CONSOLE_MESSAGE_LEVEL = bidict(
    info=QtWebEngineWidgets.QWebEnginePage.InfoMessageLevel,
    warning=QtWebEngineWidgets.QWebEnginePage.WarningMessageLevel,
    error=QtWebEngineWidgets.QWebEnginePage.ErrorMessageLevel,
)

LIFECYCLE_STATE = bidict(
    active=QtWebEngineWidgets.QWebEnginePage.LifecycleState.Active,
    frozen=QtWebEngineWidgets.QWebEnginePage.LifecycleState.Frozen,
    discarded=QtWebEngineWidgets.QWebEnginePage.LifecycleState.Discarded,
)

LifecycleStateStr = Literal["active", "frozen", "discarded"]

NAVIGATION_TYPES = bidict(
    link_clicked=QtWebEngineWidgets.QWebEnginePage.NavigationTypeLinkClicked,
    typed=QtWebEngineWidgets.QWebEnginePage.NavigationTypeTyped,
    form_submitted=QtWebEngineWidgets.QWebEnginePage.NavigationTypeFormSubmitted,
    back_forward=QtWebEngineWidgets.QWebEnginePage.NavigationTypeBackForward,
    reload=QtWebEngineWidgets.QWebEnginePage.NavigationTypeReload,
    redirect=QtWebEngineWidgets.QWebEnginePage.NavigationTypeRedirect,
    other=QtWebEngineWidgets.QWebEnginePage.NavigationTypeOther,
)

PERMISSION_POLICY = bidict(
    unknown=QtWebEngineWidgets.QWebEnginePage.PermissionUnknown,
    granted_by_user=QtWebEngineWidgets.QWebEnginePage.PermissionGrantedByUser,
    denied_by_user=QtWebEngineWidgets.QWebEnginePage.PermissionDeniedByUser,
)

PermissionPolicyStr = Literal["unknown", "granted_by_user", "denied_by_user"]

RENDER_PROCESS_TERMINATION_STATUS = bidict(
    normal=QtWebEngineWidgets.QWebEnginePage.NormalTerminationStatus,
    abnormal=QtWebEngineWidgets.QWebEnginePage.AbnormalTerminationStatus,
    crashed=QtWebEngineWidgets.QWebEnginePage.CrashedTerminationStatus,
    killed=QtWebEngineWidgets.QWebEnginePage.KilledTerminationStatus,
)

WEB_ACTION = bidict(
    none=QtWebEngineWidgets.QWebEnginePage.NoWebAction,
    back=QtWebEngineWidgets.QWebEnginePage.Back,
    forward=QtWebEngineWidgets.QWebEnginePage.Forward,
    stop=QtWebEngineWidgets.QWebEnginePage.Stop,
    reload=QtWebEngineWidgets.QWebEnginePage.Reload,
    reload_and_bypass_cache=QtWebEngineWidgets.QWebEnginePage.ReloadAndBypassCache,
    cut=QtWebEngineWidgets.QWebEnginePage.Cut,
    copy=QtWebEngineWidgets.QWebEnginePage.Copy,
    paste=QtWebEngineWidgets.QWebEnginePage.Paste,
    undo=QtWebEngineWidgets.QWebEnginePage.Undo,
    redo=QtWebEngineWidgets.QWebEnginePage.Redo,
    select_all=QtWebEngineWidgets.QWebEnginePage.SelectAll,
    paste_and_match_style=QtWebEngineWidgets.QWebEnginePage.PasteAndMatchStyle,
    open_link_in_this_window=QtWebEngineWidgets.QWebEnginePage.OpenLinkInThisWindow,
    open_link_in_new_window=QtWebEngineWidgets.QWebEnginePage.OpenLinkInNewWindow,
    open_link_in_new_tab=QtWebEngineWidgets.QWebEnginePage.OpenLinkInNewTab,
    open_link_in_new_bg_tab=QtWebEngineWidgets.QWebEnginePage.OpenLinkInNewBackgroundTab,
    copy_link_to_clipboard=QtWebEngineWidgets.QWebEnginePage.CopyLinkToClipboard,
    copy_image_to_clipboard=QtWebEngineWidgets.QWebEnginePage.CopyImageToClipboard,
    copy_image_url_to_clipboard=QtWebEngineWidgets.QWebEnginePage.CopyImageUrlToClipboard,
    copy_media_url_to_clipboard=QtWebEngineWidgets.QWebEnginePage.CopyMediaUrlToClipboard,
    toggle_media_controls=QtWebEngineWidgets.QWebEnginePage.ToggleMediaControls,
    toggle_media_loop=QtWebEngineWidgets.QWebEnginePage.ToggleMediaLoop,
    toggle_media_play_pause=QtWebEngineWidgets.QWebEnginePage.ToggleMediaPlayPause,
    toggle_media_mute=QtWebEngineWidgets.QWebEnginePage.ToggleMediaMute,
    download_link_to_disk=QtWebEngineWidgets.QWebEnginePage.DownloadLinkToDisk,
    download_image_to_disk=QtWebEngineWidgets.QWebEnginePage.DownloadImageToDisk,
    download_media_to_disk=QtWebEngineWidgets.QWebEnginePage.DownloadMediaToDisk,
    inspect_element=QtWebEngineWidgets.QWebEnginePage.InspectElement,
    exit_fullscreen=QtWebEngineWidgets.QWebEnginePage.ExitFullScreen,
    request_close=QtWebEngineWidgets.QWebEnginePage.RequestClose,
    unselect=QtWebEngineWidgets.QWebEnginePage.Unselect,
    save_page=QtWebEngineWidgets.QWebEnginePage.SavePage,
    view_source=QtWebEngineWidgets.QWebEnginePage.ViewSource,
    toggle_bold=QtWebEngineWidgets.QWebEnginePage.ToggleBold,
    toggle_italic=QtWebEngineWidgets.QWebEnginePage.ToggleItalic,
    toggle_underline=QtWebEngineWidgets.QWebEnginePage.ToggleUnderline,
    toggle_strikethrough=QtWebEngineWidgets.QWebEnginePage.ToggleStrikethrough,
    align_left=QtWebEngineWidgets.QWebEnginePage.AlignLeft,
    align_center=QtWebEngineWidgets.QWebEnginePage.AlignCenter,
    align_right=QtWebEngineWidgets.QWebEnginePage.AlignRight,
    align_justified=QtWebEngineWidgets.QWebEnginePage.AlignJustified,
    indent=QtWebEngineWidgets.QWebEnginePage.Indent,
    outdent=QtWebEngineWidgets.QWebEnginePage.Outdent,
    insert_ordered_list=QtWebEngineWidgets.QWebEnginePage.InsertOrderedList,
    insert_unordered_list=QtWebEngineWidgets.QWebEnginePage.InsertUnorderedList,
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

WEB_WINDOW_TYPES = bidict(
    browser_window=QtWebEngineWidgets.QWebEnginePage.WebBrowserWindow,
    browser_tab=QtWebEngineWidgets.QWebEnginePage.WebBrowserTab,
    dialog=QtWebEngineWidgets.QWebEnginePage.WebDialog,
    browser_bg_tab=QtWebEngineWidgets.QWebEnginePage.WebBrowserBackgroundTab,
)


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    """A web engine page holds the HTML document contents, link history + actions."""

    def serialize_fields(self):
        return dict(
            audio_muted=self.isAudioMuted(),
            background_color=self.backgroundColor(),
            # has_selection=self.hasSelection(),
            lifecycle_state=self.get_lifecycle_state(),
            # scroll_position=self.scrollPosition(),
            url=core.Url(self.url()),
            visible=self.isVisible(),
            history=core.DataStream.create_bytearray(self.history()),
            zoom_factor=self.zoomFactor(),
        )

    def get_icon(self) -> gui.Icon:
        return gui.Icon(self.icon())

    def set_url(self, url: Union[str, pathlib.Path]):
        """Set the url of the WebEnginePage.

        Clears the Page and loads the URL.

        Args:
            url: URL to set
        """
        if isinstance(url, pathlib.Path):
            url = core.Url.fromLocalFile(str(url))
        elif isinstance(url, str):
            url = core.Url(url)
        self.setUrl(url)

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

    def load_url(self, url: Union[str, pathlib.Path]):
        """Load the URL.

        Loads the specified url and displays it.

        Note: The Page remains the same until enough data has arrived
        to display the new URL.

        Args:
            url: URL to load
        """
        if isinstance(url, pathlib.Path):
            url = core.Url.fromLocalFile(str(url))
        elif isinstance(url, str):
            url = core.Url(url)
        self.load(url)

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
        callback: Callable[[bool], None] = None,
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
        flag = self.FindFlag()
        if case_sensitive:
            flag |= self.FindCaseSensitively
        if backward:
            flag |= self.FindBackward
        self.findText(string, flag, callback)

    def set_lifecycle_state(self, state: LifecycleStateStr):
        """Set lifecycle state.

        Args:
            state: lifecycle state

        Raises:
            InvalidParamError: lifecycle state does not exist
        """
        if state not in LIFECYCLE_STATE:
            raise InvalidParamError(state, LIFECYCLE_STATE)
        self.setLifecycleState(LIFECYCLE_STATE[state])

    def get_lifecycle_state(self) -> LifecycleStateStr:
        """Get the current lifecycle state.

        Returns:
            lifecycle state
        """
        return LIFECYCLE_STATE.inverse[self.lifecycleState()]

    def trigger_action(self, action: WebActionStr, checked: bool = False):
        self.triggerAction(WEB_ACTION[action], checked)

    def set_feature_permission(
        self,
        url: Union[QtCore.QUrl, str],
        feature: FeatureStr,
        policy: PermissionPolicyStr,
    ):
        url = core.Url(url)
        self.setFeaturePermission(url, FEATURE[feature], PERMISSION_POLICY[policy])

    def get_history(self) -> webenginewidgets.WebEngineHistory:
        hist = self.history()
        return webenginewidgets.WebEngineHistory(hist)

    def get_settings(self) -> webenginewidgets.WebEngineSettings:
        settings = self.settings()
        return webenginewidgets.WebEngineSettings(settings)

    def set_setting(
        self,
        setting_name: webenginewidgets.webenginesettings.WebAttributeStr,
        value: bool,
    ):
        self.get_settings()[setting_name] = value

    def get_setting(
        self, setting_name: webenginewidgets.webenginesettings.WebAttributeStr
    ) -> bool:
        return self.get_settings()[setting_name]

    def get_scripts(self) -> webenginewidgets.WebEngineScriptCollection:
        return webenginewidgets.WebEngineScriptCollection(self.scripts())

    def get_context_menu_data(self) -> webenginewidgets.WebEngineContextMenuData:
        return webenginewidgets.WebEngineContextMenuData(self.contextMenuData())

    # def choose_files(
    #     self,
    #     mode: FileSelectionModeStr,
    #     old_files: List[str],
    #     mimetypes: List[str],
    # ) -> List[str]:
    #     if mode not in FILE_SELECTION_MODE:
    #         raise InvalidParamError(mode, FILE_SELECTION_MODE)
    #     return self.chooseFiles(FILE_SELECTION_MODE[mode], old_files, mimetypes)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    path = path = "E:\\dev\\datacook\\processanalyzer\\docs\\index.html"
    widget = WebEnginePage()
    widget.set_url(path)
    widget.find_text("test", backward=True, case_sensitive=True, callback=None)
    app.main_loop()
