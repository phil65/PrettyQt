"""Classes and functions for rendering PDF documents."""

from __future__ import annotations

from prettyqt.qt.QtPdf import *  # noqa: F403

from .pdfbookmarkmodel import PdfBookmarkModel
from .pdfdocument import PdfDocument
from .pdfsearchmodel import PdfSearchModel
from prettyqt.qt import QtPdf

QT_MODULE = QtPdf


__all__ = ["PdfBookmarkModel", "PdfDocument", "PdfSearchModel"]
