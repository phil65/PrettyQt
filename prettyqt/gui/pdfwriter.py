from typing import Optional, Tuple, Union

from qtpy import QtCore, QtGui

from prettyqt import core, gui
from prettyqt.utils import InvalidParamError


class PdfWriter(QtGui.QPdfWriter):
    def setup(self, size: QtCore.QSize):
        primary = gui.app().primaryScreen()
        dpi = primary.logicalDotsPerInchX()
        self.setResolution(int(dpi))
        self.set_page_margins((0, 0, 0, 0))
        self.setPageSizeMM(core.SizeF(size.width(), size.height()) / dpi * 25.4)

    def set_page_margins(
        self,
        margins: Union[Tuple[float, float, float, float], QtCore.QMarginsF],
        unit: Optional[str] = None,
    ):
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
    writer.setup(QtCore.QSize(1, 1))
