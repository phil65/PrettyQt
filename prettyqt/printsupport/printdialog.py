from __future__ import annotations

from prettyqt import printsupport
from prettyqt.qt import QtPrintSupport


class PrintDialog(printsupport.AbstractPrintDialogMixin, QtPrintSupport.QPrintDialog):
    pass
