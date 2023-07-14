"""Classes to make printing easier and more portable."""

from __future__ import annotations

from prettyqt.qt.QtPrintSupport import *  # noqa: F403

from .printer import Printer
from .abstractprintdialog import AbstractPrintDialog, AbstractPrintDialogMixin
from .printdialog import PrintDialog
from .pagesetupdialog import PageSetupDialog
from .printengine import PrintEngine
from .printpreviewwidget import PrintPreviewWidget
from .printpreviewdialog import PrintPreviewDialog
from prettyqt.qt import QtPrintSupport

QT_MODULE = QtPrintSupport

__all__ = [
    "Printer",
    "AbstractPrintDialog",
    "AbstractPrintDialogMixin",
    "PrintDialog",
    "PageSetupDialog",
    "PrintEngine",
    "PrintPreviewWidget",
    "PrintPreviewDialog",
]
