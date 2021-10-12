from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import InvalidParamError, bidict


Item = QtWebEngineCore.QWebEngineDownloadRequest

DOWNLOAD_INTERRUPT_REASONS = bidict(
    none=Item.DownloadInterruptReason.NoReason,
    file_failed=Item.DownloadInterruptReason.FileFailed,
    file_access_denied=Item.DownloadInterruptReason.FileAccessDenied,
    file_no_space=Item.DownloadInterruptReason.FileNoSpace,
    filename_too_long=Item.DownloadInterruptReason.FileNameTooLong,
    file_too_large=Item.DownloadInterruptReason.FileTooLarge,
    file_virus_infected=Item.DownloadInterruptReason.FileVirusInfected,
    file_transient_error=Item.DownloadInterruptReason.FileTransientError,
    file_blocked=Item.DownloadInterruptReason.FileBlocked,
    file_security_check_failed=Item.DownloadInterruptReason.FileSecurityCheckFailed,
    file_too_short=Item.DownloadInterruptReason.FileTooShort,
    file_hash_mismatch=Item.DownloadInterruptReason.FileHashMismatch,
    network_fialed=Item.DownloadInterruptReason.NetworkFailed,
    network_timeout=Item.DownloadInterruptReason.NetworkTimeout,
    network_disconnected=Item.DownloadInterruptReason.NetworkDisconnected,
    network_server_down=Item.DownloadInterruptReason.NetworkServerDown,
    network_invalid_request=Item.DownloadInterruptReason.NetworkInvalidRequest,
    server_failed=Item.DownloadInterruptReason.ServerFailed,
    server_bad_content=Item.DownloadInterruptReason.ServerBadContent,
    server_unauthorized=Item.DownloadInterruptReason.ServerUnauthorized,
    server_cert_problem=Item.DownloadInterruptReason.ServerCertProblem,
    server_forbidden=Item.DownloadInterruptReason.ServerForbidden,
    server_unreachable=Item.DownloadInterruptReason.ServerUnreachable,
    user_canceled=Item.DownloadInterruptReason.UserCanceled,
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
    requested=Item.DownloadState.DownloadRequested,
    in_progress=Item.DownloadState.DownloadInProgress,
    completed=Item.DownloadState.DownloadCompleted,
    cancelled=Item.DownloadState.DownloadCancelled,
    interrupted=Item.DownloadState.DownloadInterrupted,
)

DownloadStateStr = Literal[
    "requested", "in_progress", "completed", "cancelled", "interrupted"
]

SAVE_PAGE_FORMAT = bidict(
    unknown=Item.SavePageFormat.UnknownSaveFormat,
    single_html=Item.SavePageFormat.SingleHtmlSaveFormat,
    complete_html=Item.SavePageFormat.CompleteHtmlSaveFormat,
    mime_html=Item.SavePageFormat.MimeHtmlSaveFormat,
)

SavePageFormatStr = Literal["unknown", "single_html", "complete_html", "mime_html"]

# Item.__bases__ = (core.Object,)


class WebEngineDownloadRequest:
    def __init__(self, item: QtWebEngineCore.QWebEngineDownloadRequest):
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
