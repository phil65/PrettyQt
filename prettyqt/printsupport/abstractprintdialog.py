from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtPrintSupport
from prettyqt.utils import bidict


PRINT_RANGE = bidict(
    all_pages=QtPrintSupport.QAbstractPrintDialog.PrintRange.AllPages,
    selection=QtPrintSupport.QAbstractPrintDialog.PrintRange.Selection,
    page_range=QtPrintSupport.QAbstractPrintDialog.PrintRange.PageRange,
    current_page=QtPrintSupport.QAbstractPrintDialog.PrintRange.CurrentPage,
)

PrintRangeStr = Literal["all_pages", "selection", "page_range", "current_page"]

PRINT_DIALOG_OPTION = bidict(
    to_file=QtPrintSupport.QAbstractPrintDialog.PrintDialogOption.PrintToFile,
    selection=QtPrintSupport.QAbstractPrintDialog.PrintDialogOption.PrintSelection,
    page_range=QtPrintSupport.QAbstractPrintDialog.PrintDialogOption.PrintPageRange,
    show_page_size=QtPrintSupport.QAbstractPrintDialog.PrintDialogOption.PrintShowPageSize,
    collate_copies=QtPrintSupport.QAbstractPrintDialog.PrintDialogOption.PrintCollateCopies,
    current_page=QtPrintSupport.QAbstractPrintDialog.PrintDialogOption.PrintCurrentPage,
)

PrintDialogOptionStr = Literal[
    "to_file",
    "selection",
    "page_range",
    "show_page_size",
    "collate_copies",
    "current_page",
]


class AbstractPrintDialogMixin(widgets.DialogMixin):
    def get_print_range(self) -> PrintRangeStr:
        return PRINT_RANGE.inverse[self.printRange()]

    def set_print_range(
        self, print_range: PrintRangeStr | QtPrintSupport.QAbstractPrintDialog.PrintRange
    ):
        """Set print range.

        Args:
            print_range: print range
        """
        self.setPrintRange(PRINT_RANGE.get_enum_value(print_range))


class AbstractPrintDialog(AbstractPrintDialogMixin, QtPrintSupport.QAbstractPrintDialog):
    pass
