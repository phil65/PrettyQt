from typing import Literal

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

# from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


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

DownloadInterruptReasonStr = Literal[
    "none",
    "file_failed",
    "file_access_denied",
    "file_no_space",
    "filename_too_long",
    "file_too_large",
    "file_virus_infected",
    "file_transient_error",
    "file_blocked",
    "file_security_check_failed",
    "file_too_short",
    "file_hash_mismatch",
    "network_fialed",
    "network_timeout",
    "network_disconnected",
    "network_server_down",
    "network_invalid_request",
    "server_failed",
    "server_bad_content",
    "server_unauthorized",
    "server_cert_problem",
    "server_forbidden",
    "server_unreachable",
    "user_canceled",
]

DOWNLOAD_STATE = bidict(
    requested=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested,
    in_progress=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadInProgress,
    completed=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadCompleted,
    cancelled=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadCancelled,
    interrupted=QtWebEngineWidgets.QWebEngineDownloadItem.DownloadInterrupted,
)

DownloadStateStr = Literal[
    "requested", "in_progress", "completed", "cancelled", "interrupted"
]

SAVE_PAGE_FORMAT = bidict(
    unknown=QtWebEngineWidgets.QWebEngineDownloadItem.UnknownSaveFormat,
    single_html=QtWebEngineWidgets.QWebEngineDownloadItem.SingleHtmlSaveFormat,
    complete_html=QtWebEngineWidgets.QWebEngineDownloadItem.CompleteHtmlSaveFormat,
    mime_html=QtWebEngineWidgets.QWebEngineDownloadItem.MimeHtmlSaveFormat,
)

SavePageFormatStr = Literal["unknown", "single_html", "complete_html", "mime_html"]

# QtWebEngineWidgets.QWebEngineDownloadItem.__bases__ = (core.Object,)


class WebEngineDownloadItem:
    def __init__(self, item: QtWebEngineWidgets.QWebEngineDownloadItem):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_interrupt_reason(self) -> DownloadInterruptReasonStr:
        return DOWNLOAD_INTERRUPT_REASONS.inverse[self.item.interruptReason()]

    def get_state(self) -> DownloadStateStr:
        return DOWNLOAD_STATE.inverse[self.item.state()]

    def set_save_page_format(self, fmt: SavePageFormatStr):
        """Set the save page format.

        Args:
            fmt: save page format for the layout

        Raises:
            InvalidParamError: save page format does not exist
        """
        if fmt not in SAVE_PAGE_FORMAT:
            raise InvalidParamError(fmt, SAVE_PAGE_FORMAT)
        self.item.setSavePageFormat(SAVE_PAGE_FORMAT[fmt])

    def get_save_page_format(self) -> SavePageFormatStr:
        """Return current save page format.

        Returns:
            Save page format
        """
        return SAVE_PAGE_FORMAT.inverse[self.item.savePageFormat()]


# if __name__ == "__main__":
#     from prettyqt import widgets

# app = widgets.app()
# item = WebEngineDownloadItem()
# app.main_loop()
