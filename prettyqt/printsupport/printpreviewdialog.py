from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtPrintSupport


class PrintPreviewDialog(widgets.DialogMixin, QtPrintSupport.QPrintPreviewDialog):
    pass
