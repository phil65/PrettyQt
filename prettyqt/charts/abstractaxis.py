from __future__ import annotations

from typing import Optional

from prettyqt import constants, core, gui
from prettyqt.qt.QtCharts import QtCharts


QtCharts.QAbstractAxis.__bases__ = (core.Object,)


class AbstractAxis(QtCharts.QAbstractAxis):
    def get_alignment(self) -> Optional[constants.SideStr]:
        """Return current alignment.

        Returns:
            alignment
        """
        alignment = self.alignment()
        if int(alignment) == 0:
            return None
        return constants.SIDES.inverse[alignment]

    def get_orientation(self) -> Optional[constants.OrientationStr]:
        """Return current orientation.

        Returns:
            orientation
        """
        orientation = self.orientation()
        if int(orientation) == 0:
            return None
        return constants.ORIENTATION.inverse[orientation]

    def get_grid_line_color(self) -> gui.Color:
        return gui.Color(self.gridLineColor())

    def get_grid_line_pen(self) -> gui.Pen:
        return gui.Pen(self.gridLinePen())

    def get_line_pen(self) -> gui.Pen:
        return gui.Pen(self.linePen())

    def get_line_pen_color(self) -> gui.Color:
        return gui.Color(self.linePenColor())

    def get_labels_color(self) -> gui.Color:
        return gui.Color(self.labelsColor())

    def get_labels_brush(self) -> gui.Brush:
        return gui.Brush(self.labelsBrush())

    def get_labels_font(self) -> gui.Font:
        return gui.Font(self.labelsFont())

    def get_title_font(self) -> gui.Font:
        return gui.Font(self.titleFont())

    def get_title_brush(self) -> gui.Brush:
        return gui.Brush(self.titleBrush())

    def get_shades_color(self) -> gui.Color:
        return gui.Color(self.shadesColor())

    def get_shades_brush(self) -> gui.Brush:
        return gui.Brush(self.shadesBrush())

    def get_shades_pen(self) -> gui.Pen:
        return gui.Pen(self.shadesPen())

    def get_shades_border_color(self) -> gui.Color:
        return gui.Color(self.shadesBorderColor())

    def get_minor_grid_line_pen(self) -> gui.Pen:
        return gui.Pen(self.minorGridLinePen())

    def get_minor_grid_line_color(self) -> gui.Color:
        return gui.Color(self.minorGridLineColor())
