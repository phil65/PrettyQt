from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtPrintSupport


class PrintPreviewDialog(widgets.DialogMixin, QtPrintSupport.QPrintPreviewDialog):
    """Dialog for previewing and configuring page layouts for printer output."""

    @classmethod
    def setup_example(cls):
        return None


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    dlg = PrintPreviewDialog()
    dlg.show()
