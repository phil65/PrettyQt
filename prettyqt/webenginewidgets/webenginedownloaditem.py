# -*- coding: utf-8 -*-

try:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
except ImportError:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

Item = QtWebEngineWidgets.QWebEngineDownloadItem

DOWNLOAD_INTERRUPT_REASONS = bidict(
    none=Item.NoReason,
    file_failed=Item.FileFailed,
    file_access_denied=Item.FileAccessDenied,
    file_no_space=Item.FileNoSpace,
    filename_too_long=Item.FileNameTooLong,
    file_too_large=Item.FileTooLarge,
    file_virus_infected=Item.FileVirusInfected,
    file_transient_error=Item.FileTransientError,
    file_blocked=Item.FileBlocked,
    file_security_check_failed=Item.FileSecurityCheckFailed,
    file_too_short=Item.FileTooShort,
    file_hash_mismatch=Item.FileHashMismatch,
    network_fialed=Item.NetworkFailed,
    network_timeout=Item.NetworkTimeout,
    network_disconnected=Item.NetworkDisconnected,
    network_server_down=Item.NetworkServerDown,
    network_invalid_request=Item.NetworkInvalidRequest,
    server_failed=Item.ServerFailed,
    server_bad_content=Item.ServerBadContent,
    server_unauthorized=Item.ServerUnauthorized,
    server_cert_problem=Item.ServerCertProblem,
    server_forbidden=Item.ServerForbidden,
    server_unreachable=Item.ServerUnreachable,
    user_canceled=Item.UserCanceled,
)

DOWNLOAD_STATES = bidict(
    requested=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested,
    in_progress=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadInProgress,
    completed=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadCompleted,
    cancelled=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadCancelled,
    interrupted=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadInterrupted,
)

SAVE_PAGE_FORMATS = bidict(
    unknown=QtWebEngineWidgets.QWebEngineDownloadItem.UnknownSaveFormat,
    single_html=QtWebEngineWidgets.QWebEngineDownloadItem.SingleHtmlSaveFormat,
    complete_html=QtWebEngineWidgets.QWebEngineDownloadItem.CompleteHtmlSaveFormat,
    mime_html=QtWebEngineWidgets.QWebEngineDownloadItem.MimeHtmlSaveFormat,
)

QtWebEngineWidgets.QWebEngineDownloadItem.__bases__ = (core.Object,)


class WebEngineDownloadItem(QtWebEngineWidgets.QWebEngineDownloadItem):
    def get_interrupt_reason(self) -> str:
        return DOWNLOAD_INTERRUPT_REASONS.inv[self.interruptReason()]

    def get_state(self) -> str:
        return DOWNLOAD_STATES.inv[self.state()]

    def set_save_page_format(self, fmt: str):
        """Set the save page format.

        Allowed values are "unknown", "single_html", "complete_html", "mime_html"

        Args:
            fmt: save page format for the layout

        Raises:
            InvalidParamError: save page format does not exist
        """
        if fmt not in SAVE_PAGE_FORMATS:
            raise InvalidParamError(fmt, SAVE_PAGE_FORMATS)
        self.setSavePageFormat(SAVE_PAGE_FORMATS[fmt])

    def get_save_page_format(self) -> str:
        """Return current save page format.

        Possible values are "unknown", "single_html", "complete_html", "mime_html"

        Returns:
            Save page format
        """
        return SAVE_PAGE_FORMATS.inv[self.savePageFormat()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = WebEngineDownloadItem()
    app.main_loop()
