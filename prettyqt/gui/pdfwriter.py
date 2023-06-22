from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, datatypes


class PdfWriter(core.ObjectMixin, gui.PagedPaintDeviceMixin, QtGui.QPdfWriter):
    def set_desktop_resolution(self):
        primary = gui.app().primaryScreen()
        dpi = primary.logicalDotsPerInch()
        self.setResolution(int(dpi))

    def set_page_margins(
        self,
        margins: datatypes.MarginsFType,
        unit: gui.pagelayout.UnitStr | None = None,
    ) -> bool:
        margins = datatypes.to_marginsf(margins)
        if unit is None:
            return self.setPageMargins(margins)
        if unit not in gui.pagelayout.UNITS:
            raise InvalidParamError(unit, gui.pagelayout.UNITS)
        return self.setPageMargins(margins, gui.pagelayout.UNITS[unit])

    def get_pdf_version(self) -> gui.pagedpaintdevice.PdfVersionStr:
        return gui.pagedpaintdevice.PDF_VERSION.inverse[self.pdfVersion()]

    def set_pdf_version(self, version: gui.pagedpaintdevice.PdfVersionStr):
        """Set pdf version.

        Args:
            version: pdf version

        Raises:
            InvalidParamError: pdf version does not exist
        """
        if version not in gui.pagedpaintdevice.PDF_VERSION:
            raise InvalidParamError(version, gui.pagedpaintdevice.PDF_VERSION)
        self.setPdfVersion(gui.pagedpaintdevice.PDF_VERSION[version])


if __name__ == "__main__":
    app = gui.app()
    writer = PdfWriter("")
    writer.set_desktop_resolution()
