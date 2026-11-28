import mimetypes
import os
from typing import Literal, Self

from prettyqt import core, gui
from prettyqt.utils import bidict, datatypes, get_repr, serializemixin


MODE = bidict(
    normal=gui.QIcon.Mode.Normal,
    disabled=gui.QIcon.Mode.Disabled,
    active=gui.QIcon.Mode.Active,
    selected=gui.QIcon.Mode.Selected,
)

ModeStr = Literal["normal", "disabled", "active", "selected"]

STATE = bidict(off=gui.QIcon.State.Off, on=gui.QIcon.State.On)

StateStr = Literal["off", "on"]

ThemeIconStr = Literal[
    "address_book_new",
    "application_exit",
    "appointment_new",
    "call_start",
    "call_stop",
    "contact_new",
    "document_new",
    "document_open",
    "document_open_recent",
    "document_page_setup",
    "document_print",
    "document_print_preview",
    "document_properties",
    "document_revert",
    "document_save",
    "document_save_as",
    "document_send",
    "edit_clear",
    "edit_copy",
    "edit_cut",
    "edit_delete",
    "edit_find",
    "edit_paste",
    "edit_redo",
    "edit_select_all",
    "edit_undo",
    "folder_new",
    "format_indent_less",
    "format_indent_more",
    "format_justify_center",
    "format_justify_fill",
    "format_justify_left",
    "format_justify_right",
    "format_text_direction_ltr",
    "format_text_direction_rtl",
    "format_text_bold",
    "format_text_italic",
    "format_text_underline",
    "format_text_strikethrough",
    "go_down",
    "go_home",
    "go_next",
    "go_previous",
    "go_up",
    "help_about",
    "help_faq",
    "insert_image",
    "insert_link",
    "insert_text",
    "list_add",
    "list_remove",
    "mail_forward",
    "mail_mark_important",
    "mail_mark_read",
    "mail_mark_unread",
    "mail_message_new",
    "mail_reply_all",
    "mail_reply_sender",
    "mail_send",
    "media_eject",
    "media_playback_pause",
    "media_playback_start",
    "media_playback_stop",
    "media_record",
    "media_seek_backward",
    "media_seek_forward",
    "media_skip_backward",
    "media_skip_forward",
    "object_rotate_left",
    "object_rotate_right",
    "process_stop",
    "system_lock_screen",
    "system_log_out",
    "system_search",
    "system_reboot",
    "system_shutdown",
    "tools_check_spelling",
    "view_fullscreen",
    "view_refresh",
    "view_restore",
    "window_close",
    "window_new",
    "zoom_fit_best",
    "zoom_in",
    "zoom_out",
    "audio_card",
    "audio_input_microphone",
    "battery",
    "camera_photo",
    "camera_video",
    "camera_web",
    "computer",
    "drive_harddisk",
    "drive_optical",
    "input_gaming",
    "input_keyboard",
    "input_mouse",
    "input_tablet",
    "media_flash",
    "media_optical",
    "media_tape",
    "multimedia_player",
    "network_wired",
    "network_wireless",
    "phone",
    "printer",
    "scanner",
    "video_display",
    "appointment_missed",
    "appointment_soon",
    "audio_volume_high",
    "audio_volume_low",
    "audio_volume_medium",
    "audio_volume_muted",
    "battery_caution",
    "battery_low",
    "dialog_error",
    "dialog_information",
    "dialog_password",
    "dialog_question",
    "dialog_warning",
    "folder_drag_accept",
    "folder_open",
    "folder_visiting",
    "image_loading",
    "image_missing",
    "mail_attachment",
    "mail_unread",
    "mail_read",
    "mail_replied",
    "media_playlist_repeat",
    "media_playlist_shuffle",
    "network_offline",
    "printer_printing",
    "security_high",
    "security_low",
    "software_update_available",
    "software_update_urgent",
    "sync_error",
    "sync_synchronizing",
    "user_available",
    "user_offline",
    "weather_clear",
    "weather_clear_night",
    "weather_few_clouds",
    "weather_few_clouds_night",
    "weather_fog",
    "weather_showers",
    "weather_snow",
    "weather_storm",
]

THEME_ICON: bidict[ThemeIconStr, gui.QIcon.ThemeIcon] = bidict(
    address_book_new=gui.QIcon.ThemeIcon.AddressBookNew,
    application_exit=gui.QIcon.ThemeIcon.ApplicationExit,
    appointment_new=gui.QIcon.ThemeIcon.AppointmentNew,
    call_start=gui.QIcon.ThemeIcon.CallStart,
    call_stop=gui.QIcon.ThemeIcon.CallStop,
    contact_new=gui.QIcon.ThemeIcon.ContactNew,
    document_new=gui.QIcon.ThemeIcon.DocumentNew,
    document_open=gui.QIcon.ThemeIcon.DocumentOpen,
    document_open_recent=gui.QIcon.ThemeIcon.DocumentOpenRecent,
    document_page_setup=gui.QIcon.ThemeIcon.DocumentPageSetup,
    document_print=gui.QIcon.ThemeIcon.DocumentPrint,
    document_print_preview=gui.QIcon.ThemeIcon.DocumentPrintPreview,
    document_properties=gui.QIcon.ThemeIcon.DocumentProperties,
    document_revert=gui.QIcon.ThemeIcon.DocumentRevert,
    document_save=gui.QIcon.ThemeIcon.DocumentSave,
    document_save_as=gui.QIcon.ThemeIcon.DocumentSaveAs,
    document_send=gui.QIcon.ThemeIcon.DocumentSend,
    edit_clear=gui.QIcon.ThemeIcon.EditClear,
    edit_copy=gui.QIcon.ThemeIcon.EditCopy,
    edit_cut=gui.QIcon.ThemeIcon.EditCut,
    edit_delete=gui.QIcon.ThemeIcon.EditDelete,
    edit_find=gui.QIcon.ThemeIcon.EditFind,
    edit_paste=gui.QIcon.ThemeIcon.EditPaste,
    edit_redo=gui.QIcon.ThemeIcon.EditRedo,
    edit_select_all=gui.QIcon.ThemeIcon.EditSelectAll,
    edit_undo=gui.QIcon.ThemeIcon.EditUndo,
    folder_new=gui.QIcon.ThemeIcon.FolderNew,
    format_indent_less=gui.QIcon.ThemeIcon.FormatIndentLess,
    format_indent_more=gui.QIcon.ThemeIcon.FormatIndentMore,
    format_justify_center=gui.QIcon.ThemeIcon.FormatJustifyCenter,
    format_justify_fill=gui.QIcon.ThemeIcon.FormatJustifyFill,
    format_justify_left=gui.QIcon.ThemeIcon.FormatJustifyLeft,
    format_justify_right=gui.QIcon.ThemeIcon.FormatJustifyRight,
    format_text_direction_ltr=gui.QIcon.ThemeIcon.FormatTextDirectionLtr,
    format_text_direction_rtl=gui.QIcon.ThemeIcon.FormatTextDirectionRtl,
    format_text_bold=gui.QIcon.ThemeIcon.FormatTextBold,
    format_text_italic=gui.QIcon.ThemeIcon.FormatTextItalic,
    format_text_underline=gui.QIcon.ThemeIcon.FormatTextUnderline,
    format_text_strikethrough=gui.QIcon.ThemeIcon.FormatTextStrikethrough,
    go_down=gui.QIcon.ThemeIcon.GoDown,
    go_home=gui.QIcon.ThemeIcon.GoHome,
    go_next=gui.QIcon.ThemeIcon.GoNext,
    go_previous=gui.QIcon.ThemeIcon.GoPrevious,
    go_up=gui.QIcon.ThemeIcon.GoUp,
    help_about=gui.QIcon.ThemeIcon.HelpAbout,
    help_faq=gui.QIcon.ThemeIcon.HelpFaq,
    insert_image=gui.QIcon.ThemeIcon.InsertImage,
    insert_link=gui.QIcon.ThemeIcon.InsertLink,
    insert_text=gui.QIcon.ThemeIcon.InsertText,
    list_add=gui.QIcon.ThemeIcon.ListAdd,
    list_remove=gui.QIcon.ThemeIcon.ListRemove,
    mail_forward=gui.QIcon.ThemeIcon.MailForward,
    mail_mark_important=gui.QIcon.ThemeIcon.MailMarkImportant,
    mail_mark_read=gui.QIcon.ThemeIcon.MailMarkRead,
    mail_mark_unread=gui.QIcon.ThemeIcon.MailMarkUnread,
    mail_message_new=gui.QIcon.ThemeIcon.MailMessageNew,
    mail_reply_all=gui.QIcon.ThemeIcon.MailReplyAll,
    mail_reply_sender=gui.QIcon.ThemeIcon.MailReplySender,
    mail_send=gui.QIcon.ThemeIcon.MailSend,
    media_eject=gui.QIcon.ThemeIcon.MediaEject,
    media_playback_pause=gui.QIcon.ThemeIcon.MediaPlaybackPause,
    media_playback_start=gui.QIcon.ThemeIcon.MediaPlaybackStart,
    media_playback_stop=gui.QIcon.ThemeIcon.MediaPlaybackStop,
    media_record=gui.QIcon.ThemeIcon.MediaRecord,
    media_seek_backward=gui.QIcon.ThemeIcon.MediaSeekBackward,
    media_seek_forward=gui.QIcon.ThemeIcon.MediaSeekForward,
    media_skip_backward=gui.QIcon.ThemeIcon.MediaSkipBackward,
    media_skip_forward=gui.QIcon.ThemeIcon.MediaSkipForward,
    object_rotate_left=gui.QIcon.ThemeIcon.ObjectRotateLeft,
    object_rotate_right=gui.QIcon.ThemeIcon.ObjectRotateRight,
    process_stop=gui.QIcon.ThemeIcon.ProcessStop,
    system_lock_screen=gui.QIcon.ThemeIcon.SystemLockScreen,
    system_log_out=gui.QIcon.ThemeIcon.SystemLogOut,
    system_search=gui.QIcon.ThemeIcon.SystemSearch,
    system_reboot=gui.QIcon.ThemeIcon.SystemReboot,
    system_shutdown=gui.QIcon.ThemeIcon.SystemShutdown,
    tools_check_spelling=gui.QIcon.ThemeIcon.ToolsCheckSpelling,
    view_fullscreen=gui.QIcon.ThemeIcon.ViewFullscreen,
    view_refresh=gui.QIcon.ThemeIcon.ViewRefresh,
    view_restore=gui.QIcon.ThemeIcon.ViewRestore,
    window_close=gui.QIcon.ThemeIcon.WindowClose,
    window_new=gui.QIcon.ThemeIcon.WindowNew,
    zoom_fit_best=gui.QIcon.ThemeIcon.ZoomFitBest,
    zoom_in=gui.QIcon.ThemeIcon.ZoomIn,
    zoom_out=gui.QIcon.ThemeIcon.ZoomOut,
    audio_card=gui.QIcon.ThemeIcon.AudioCard,
    audio_input_microphone=gui.QIcon.ThemeIcon.AudioInputMicrophone,
    battery=gui.QIcon.ThemeIcon.Battery,
    camera_photo=gui.QIcon.ThemeIcon.CameraPhoto,
    camera_video=gui.QIcon.ThemeIcon.CameraVideo,
    camera_web=gui.QIcon.ThemeIcon.CameraWeb,
    computer=gui.QIcon.ThemeIcon.Computer,
    drive_harddisk=gui.QIcon.ThemeIcon.DriveHarddisk,
    drive_optical=gui.QIcon.ThemeIcon.DriveOptical,
    input_gaming=gui.QIcon.ThemeIcon.InputGaming,
    input_keyboard=gui.QIcon.ThemeIcon.InputKeyboard,
    input_mouse=gui.QIcon.ThemeIcon.InputMouse,
    input_tablet=gui.QIcon.ThemeIcon.InputTablet,
    media_flash=gui.QIcon.ThemeIcon.MediaFlash,
    media_optical=gui.QIcon.ThemeIcon.MediaOptical,
    media_tape=gui.QIcon.ThemeIcon.MediaTape,
    multimedia_player=gui.QIcon.ThemeIcon.MultimediaPlayer,
    network_wired=gui.QIcon.ThemeIcon.NetworkWired,
    network_wireless=gui.QIcon.ThemeIcon.NetworkWireless,
    phone=gui.QIcon.ThemeIcon.Phone,
    printer=gui.QIcon.ThemeIcon.Printer,
    scanner=gui.QIcon.ThemeIcon.Scanner,
    video_display=gui.QIcon.ThemeIcon.VideoDisplay,
    appointment_missed=gui.QIcon.ThemeIcon.AppointmentMissed,
    appointment_soon=gui.QIcon.ThemeIcon.AppointmentSoon,
    audio_volume_high=gui.QIcon.ThemeIcon.AudioVolumeHigh,
    audio_volume_low=gui.QIcon.ThemeIcon.AudioVolumeLow,
    audio_volume_medium=gui.QIcon.ThemeIcon.AudioVolumeMedium,
    audio_volume_muted=gui.QIcon.ThemeIcon.AudioVolumeMuted,
    battery_caution=gui.QIcon.ThemeIcon.BatteryCaution,
    battery_low=gui.QIcon.ThemeIcon.BatteryLow,
    dialog_error=gui.QIcon.ThemeIcon.DialogError,
    dialog_information=gui.QIcon.ThemeIcon.DialogInformation,
    dialog_password=gui.QIcon.ThemeIcon.DialogPassword,
    dialog_question=gui.QIcon.ThemeIcon.DialogQuestion,
    dialog_warning=gui.QIcon.ThemeIcon.DialogWarning,
    folder_drag_accept=gui.QIcon.ThemeIcon.FolderDragAccept,
    folder_open=gui.QIcon.ThemeIcon.FolderOpen,
    folder_visiting=gui.QIcon.ThemeIcon.FolderVisiting,
    image_loading=gui.QIcon.ThemeIcon.ImageLoading,
    image_missing=gui.QIcon.ThemeIcon.ImageMissing,
    mail_attachment=gui.QIcon.ThemeIcon.MailAttachment,
    mail_unread=gui.QIcon.ThemeIcon.MailUnread,
    mail_read=gui.QIcon.ThemeIcon.MailRead,
    mail_replied=gui.QIcon.ThemeIcon.MailReplied,
    media_playlist_repeat=gui.QIcon.ThemeIcon.MediaPlaylistRepeat,
    media_playlist_shuffle=gui.QIcon.ThemeIcon.MediaPlaylistShuffle,
    network_offline=gui.QIcon.ThemeIcon.NetworkOffline,
    printer_printing=gui.QIcon.ThemeIcon.PrinterPrinting,
    security_high=gui.QIcon.ThemeIcon.SecurityHigh,
    security_low=gui.QIcon.ThemeIcon.SecurityLow,
    software_update_available=gui.QIcon.ThemeIcon.SoftwareUpdateAvailable,
    software_update_urgent=gui.QIcon.ThemeIcon.SoftwareUpdateUrgent,
    sync_error=gui.QIcon.ThemeIcon.SyncError,
    sync_synchronizing=gui.QIcon.ThemeIcon.SyncSynchronizing,
    user_available=gui.QIcon.ThemeIcon.UserAvailable,
    user_offline=gui.QIcon.ThemeIcon.UserOffline,
    weather_clear=gui.QIcon.ThemeIcon.WeatherClear,
    weather_clear_night=gui.QIcon.ThemeIcon.WeatherClearNight,
    weather_few_clouds=gui.QIcon.ThemeIcon.WeatherFewClouds,
    weather_few_clouds_night=gui.QIcon.ThemeIcon.WeatherFewCloudsNight,
    weather_fog=gui.QIcon.ThemeIcon.WeatherFog,
    weather_showers=gui.QIcon.ThemeIcon.WeatherShowers,
    weather_snow=gui.QIcon.ThemeIcon.WeatherSnow,
    weather_storm=gui.QIcon.ThemeIcon.WeatherStorm,
)


class Icon(serializemixin.SerializeMixin, gui.QIcon):
    """Scalable icons in different modes and states."""

    def __repr__(self):
        return get_repr(self)

    def __bool__(self):
        return not self.isNull()

    def __getstate__(self):
        pixmap = self.pixmap(256, 256)
        return bytes(gui.Pixmap(pixmap))

    def __setstate__(self, ba):
        px = gui.Pixmap()
        px.__setstate__(ba)
        self.add_pixmap(px)

    @classmethod
    def for_color(cls, color_str: str) -> Self:
        color = gui.Color(color_str)
        bitmap = gui.Pixmap(16, 16)
        bitmap.fill(color)
        return cls(bitmap)

    @classmethod
    def from_char(cls, char: str, background="black", color="white") -> Self:
        """Create a QIcon with a given character."""
        icon = cls()
        for size in (16, 32, 64):
            px = gui.Pixmap.create_char(
                char, background=background, color=color, size=size
            )
            icon.addPixmap(px)
        return icon

    @classmethod
    def for_mimetype(cls, path: os.PathLike[str] | str) -> Self | None:
        """Try to create an icon from theme using the file mimetype.

        Returns None if there is no theme icon for the mimetype.
        """
        path = os.fspath(path)
        if mime := mimetypes.guess_type(path)[0]:
            name = mime.replace("/", "-")
            if cls.hasThemeIcon(name) and not (icon := cls(cls.fromTheme(name))).isNull():
                return icon
        return None

    @classmethod
    def from_theme(
        cls,
        name: ThemeIconStr | gui.QIcon.ThemeIcon | str,
        fallback: gui.QIcon | None = None,
    ) -> Self:
        """Create an icon from a theme name or Qt 6.7+ ThemeIcon."""
        if isinstance(name, str) and name in THEME_ICON:
            icon_arg: gui.QIcon.ThemeIcon | str = THEME_ICON[name]
        else:
            icon_arg = name
        if fallback is None:
            return cls(cls.fromTheme(icon_arg))
        return cls(cls.fromTheme(icon_arg, fallback))

    @classmethod
    def from_image(cls, image: gui.QImage) -> Self:
        return cls(gui.Pixmap.fromImage(image))

    def get_available_sizes(
        self,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ) -> list[core.Size]:
        m = MODE.get_enum_value(mode)
        s = STATE.get_enum_value(state)
        return [core.Size(i) for i in self.availableSizes(m, s)]

    def add_pixmap(
        self,
        data: core.QByteArray | gui.QPixmap | bytes,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ):
        if isinstance(data, bytes):
            data = core.QByteArray(data)
        if isinstance(data, core.QByteArray):
            pixmap = gui.QPixmap()
            pixmap.loadFromData(data)
        else:
            pixmap = data
        self.addPixmap(pixmap, MODE.get_enum_value(mode), STATE.get_enum_value(state))

    def get_pixmap(
        self,
        size: datatypes.SizeType | int,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ) -> gui.Pixmap:
        sz = datatypes.to_size(size)
        return gui.Pixmap(
            self.pixmap(sz, MODE.get_enum_value(mode), STATE.get_enum_value(state))
        )

    def get_actual_size(
        self,
        size: datatypes.SizeType,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ) -> core.Size:
        sz = datatypes.to_size(size)
        m = MODE.get_enum_value(mode)
        s = STATE.get_enum_value(state)
        actual_size = self.actualSize(sz, m, s)
        return core.Size(actual_size)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    icon = Icon.from_char("A")
    window = widgets.MainWindow()
    window.set_icon(icon)
    window.show()
    app.exec()
