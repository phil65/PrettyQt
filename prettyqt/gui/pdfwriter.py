from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import datatypes


class PdfWriter(core.ObjectMixin, gui.PagedPaintDeviceMixin, QtGui.QPdfWriter):
    def set_desktop_resolution(self):
        primary = gui.app().primaryScreen()
        dpi = primary.logicalDotsPerInch()
        self.setResolution(int(dpi))

    def set_page_margins(
        self,
        margins: datatypes.MarginsFType,
        unit: gui.pagelayout.UnitStr | gui.PageLayout.Unit | None = None,
    ) -> bool:
        margins = datatypes.to_marginsf(margins)
        if unit is None:
            return self.setPageMargins(margins)
        return self.setPageMargins(margins, gui.pagelayout.UNITS.get_enum_value(unit))

    def get_pdf_version(self) -> gui.pagedpaintdevice.PdfVersionStr:
        return gui.pagedpaintdevice.PDF_VERSION.inverse[self.pdfVersion()]

    def set_pdf_version(
        self,
        version: gui.pagedpaintdevice.PdfVersionStr | gui.PagedPaintDevice.PdfVersion,
    ):
        """Set pdf version.

        Args:
            version: pdf version
        """
        self.setPdfVersion(gui.pagedpaintdevice.PDF_VERSION.get_enum_value(version))


if __name__ == "__main__":
    app = gui.app()
    writer = PdfWriter("")
    writer.set_desktop_resolution()
