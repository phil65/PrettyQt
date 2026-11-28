from typing import TYPE_CHECKING, Literal

from prettyqt import gui
from prettyqt.utils import bidict


PDF_VERSION = bidict(
    v1_4=gui.QPagedPaintDevice.PdfVersion.PdfVersion_1_4,
    va1b=gui.QPagedPaintDevice.PdfVersion.PdfVersion_A1b,
    v1_6=gui.QPagedPaintDevice.PdfVersion.PdfVersion_1_6,
    vx4=gui.QPagedPaintDevice.PdfVersion.PdfVersion_X4,
)

PdfVersionStr = Literal["v1_4", "va1b", "v1_6", "vx4"]


if TYPE_CHECKING:
    from prettyqt.qt import QtGui

    _PagedPaintDeviceBase = QtGui.QPagedPaintDevice
else:
    _PagedPaintDeviceBase = object


class PagedPaintDeviceMixin(gui.PaintDeviceMixin, _PagedPaintDeviceBase):
    def get_page_ranges(self) -> gui.PageRanges:
        return gui.PageRanges(self.pageRanges())

    def get_page_layout(self) -> gui.PageLayout:
        return gui.PageLayout(self.pageLayout())

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
