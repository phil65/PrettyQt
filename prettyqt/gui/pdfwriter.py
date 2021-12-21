from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, types


QtGui.QPdfWriter.__bases__ = (core.Object, gui.PagedPaintDevice)


class PdfWriter(QtGui.QPdfWriter):
    def set_desktop_resolution(self):
        primary = gui.app().primaryScreen()
        dpi = primary.logicalDotsPerInch()
        self.setResolution(int(dpi))

    def set_page_margins(
        self,
        margins: types.MarginsFType,
        unit: gui.pagelayout.UnitStr | None = None,
    ) -> bool:
        if isinstance(margins, tuple):
            margins = QtCore.QMarginsF(*margins)
        if unit is None:
            return self.setPageMargins(margins)
        else:
            if unit not in gui.pagelayout.UNITS:
                raise InvalidParamError(unit, gui.pagelayout.UNITS)
            return self.setPageMargins(margins, gui.pagelayout.UNITS[unit])


if __name__ == "__main__":
    app = gui.app()
    writer = PdfWriter("")
    writer.set_desktop_resolution()
