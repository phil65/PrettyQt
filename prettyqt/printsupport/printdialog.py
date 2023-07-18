from __future__ import annotations

from prettyqt import printsupport


class PrintDialog(printsupport.AbstractPrintDialogMixin, printsupport.QPrintDialog):
    """Dialog for specifying the printer's configuration."""

    @classmethod
    def setup_example(cls):
        return None


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    dlg = PrintDialog()
    dlg.show()
