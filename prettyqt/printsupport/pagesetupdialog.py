from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtPrintSupport


class PageSetupDialog(widgets.DialogMixin, QtPrintSupport.QPageSetupDialog):
    """Configuration dialog for the page-related options on a printer."""

    @classmethod
    def setup_example(cls):
        return None


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    dlg = PageSetupDialog()
    dlg.show()
