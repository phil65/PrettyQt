from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


PDF_VERSION = bidict(
    v1_4=QtGui.QPagedPaintDevice.PdfVersion.PdfVersion_1_4,
    va1b=QtGui.QPagedPaintDevice.PdfVersion.PdfVersion_A1b,
    v1_6=QtGui.QPagedPaintDevice.PdfVersion.PdfVersion_1_6,
)

PdfVersionStr = Literal["v1_4", "va1b", "v1_6"]


class PagedPaintDeviceMixin(gui.PaintDeviceMixin):
    def get_page_ranges(self) -> list[gui.PageRanges]:
        return [gui.PageRanges(i) for i in self.pageRanges()]

    def get_page_layout(self) -> gui.PageLayout:
        return gui.PageLayout(self.PageLayout())

    def set_page_ranges(self, ranges: QtGui.QPageRanges | list[tuple[int, int]]):
        if isinstance(ranges, QtGui.QPageRanges):
            self.setPageRanges(ranges)
        else:
            ranges = gui.PageRanges()
            for start, end in ranges:
                ranges.addRange(start, end)

    def set_page_orientation(self, orientation: gui.pagelayout.OrientationStr):
        self.setPageOrientation(gui.pagelayout.ORIENTATIONS[orientation])


class PagedPaintDevice(PagedPaintDeviceMixin, QtGui.QPagedPaintDevice):
    pass


if __name__ == "__main__":
    device = PagedPaintDevice()
