# -*- coding: utf-8 -*-

from typing import Optional

from qtpy.QtCharts import QtCharts
from qtpy import QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict


ALIGNMENTS = bidict(
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
)

ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)


QtCharts.QAbstractAxis.__bases__ = (core.Object,)


class AbstractAxis(QtCharts.QAbstractAxis):
    def get_alignment(self) -> Optional[str]:
        """Return current alignment.

        Possible values: "left", "right", "top", "bottom"

        Returns:
            alignment
        """
        alignment = self.alignment()
        if int(alignment) == 0:
            return None
        return ALIGNMENTS.inv[alignment]

    def get_orientation(self) -> Optional[str]:
        """Return current orientation.

        Possible values: "horizontal", "vertical"

        Returns:
            orientation
        """
        orientation = self.orientation()
        if int(orientation) == 0:
            return None
        return ORIENTATIONS.inv[orientation]

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
