from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtPrintSupport


class PageSetupDialog(widgets.DialogMixin, QtPrintSupport.QPageSetupDialog):
    pass
