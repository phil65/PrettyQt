from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.utils import bidict


PDF_VERSION = bidict(
    v1_4=gui.QPagedPaintDevice.PdfVersion.PdfVersion_1_4,
    va1b=gui.QPagedPaintDevice.PdfVersion.PdfVersion_A1b,
    v1_6=gui.QPagedPaintDevice.PdfVersion.PdfVersion_1_6,
)

PdfVersionStr = Literal["v1_4", "va1b", "v1_6"]


class PagedPaintDeviceMixin(gui.PaintDeviceMixin):
    def get_page_ranges(self) -> list[gui.PageRanges]:
        return [gui.PageRanges(i) for i in self.pageRanges()]

    def get_page_layout(self) -> gui.PageLayout:
        return gui.PageLayout(self.PageLayout())

    def set_page_ranges(self, ranges: gui.QPageRanges | list[tuple[int, int]]):
        if isinstance(ranges, gui.QPageRanges):
            self.setPageRanges(ranges)
        else:
            ranges = gui.PageRanges()
            for start, end in ranges:
                ranges.addRange(start, end)

    def set_page_orientation(self, orientation: gui.pagelayout.OrientationStr):
        self.setPageOrientation(gui.pagelayout.ORIENTATIONS[orientation])


class PagedPaintDevice(PagedPaintDeviceMixin, gui.QPagedPaintDevice):
    pass


if __name__ == "__main__":
    device = PagedPaintDevice()
