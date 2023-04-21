from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtPdf
from prettyqt.utils import bidict


ERROR = bidict(
    none=QtPdf.QPdfDocument.Error.None_,
    unknown=QtPdf.QPdfDocument.Error.Unknown,
    data_not_yet_available=QtPdf.QPdfDocument.Error.DataNotYetAvailable,
    file_not_found=QtPdf.QPdfDocument.Error.FileNotFound,
    invalid_file_format=QtPdf.QPdfDocument.Error.InvalidFileFormat,
    incorrect_password=QtPdf.QPdfDocument.Error.IncorrectPassword,
    unsupported_security_scheme=QtPdf.QPdfDocument.Error.UnsupportedSecurityScheme,
)

ErrorStr = Literal[
    "none",
    "unknown",
    "data_not_yet_available",
    "file_not_found",
    "invalid_file_format",
    "incorrect_password",
    "unsupported_security_scheme",
]

STATUS = bidict(
    null=QtPdf.QPdfDocument.Status.Null,
    loading=QtPdf.QPdfDocument.Status.Loading,
    ready=QtPdf.QPdfDocument.Status.Ready,
    unloading=QtPdf.QPdfDocument.Status.Unloading,
    error=QtPdf.QPdfDocument.Status.Error,
)

StatusStr = Literal[
    "null",
    "loading",
    "ready",
    "unloading",
    "error",
]


class PdfDocument(core.ObjectMixin, QtPdf.QPdfDocument):
    def get_error(self) -> ErrorStr:
        """Return current error.

        Returns:
            page mode
        """
        return ERROR.inverse[self.error()]

    def get_status(self) -> StatusStr:
        """Return current status.

        Returns:
            zoom mode
        """
        return STATUS.inverse[self.status()]


if __name__ == "__main__":
    doc = PdfDocument()
    print(doc.get_status())
