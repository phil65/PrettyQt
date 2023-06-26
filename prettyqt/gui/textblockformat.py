from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


LineHeightTypeStr = Literal[
    "single",
    "proportional",
    "fixed",
    "minimum",
    "line_distance",
]

LINE_HEIGHT_TYPES: bidict[MarkerTypeStr, QtGui.QTextBlockFormat.LineHeightTypes] = bidict(
    single=QtGui.QTextBlockFormat.LineHeightTypes.SingleHeight,
    proportional=QtGui.QTextBlockFormat.LineHeightTypes.ProportionalHeight,
    fixed=QtGui.QTextBlockFormat.LineHeightTypes.FixedHeight,
    minimum=QtGui.QTextBlockFormat.LineHeightTypes.MinimumHeight,
    line_distance=QtGui.QTextBlockFormat.LineHeightTypes.LineDistanceHeight,
)

MarkerTypeStr = Literal[
    "none",
    "unchecked",
    "checked",
]

MARKER_TYPE: bidict[MarkerTypeStr, QtGui.QTextBlockFormat.MarkerType] = bidict(
    none=QtGui.QTextBlockFormat.MarkerType.NoMarker,
    unchecked=QtGui.QTextBlockFormat.MarkerType.Unchecked,
    checked=QtGui.QTextBlockFormat.MarkerType.Checked,
)


class TextBlockFormat(gui.TextFormatMixin, QtGui.QTextBlockFormat):
    def set_marker(self, marker: MarkerTypeStr | QtGui.QTextBlockFormat.MarkerType):
        """Set the marker.

        Args:
            marker: marker
        """
        self.setMarker(MARKER_TYPE.get_enum_value(marker))

    def get_marker(self) -> MarkerTypeStr:
        """Get current marker.

        Returns:
            current marker
        """
        return MARKER_TYPE.inverse[self.marker()]

    def set_alignment(self, alignment: constants.AlignmentStr | constants.AlignmentFlag):
        """Set the alignment of the format.

        Args:
            alignment: alignment for the format
        """
        self.setAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

    def get_alignment(self) -> constants.AlignmentStr:
        """Return current alignment.

        Returns:
            alignment
        """
        return constants.ALIGNMENTS.inverse[self.alignment()]

    def set_page_break_policy(
        self, policy: gui.textformat.PageBreakFlagStr | gui.QTextFormat.PageBreakFlag
    ):
        """Set page break policy.

        Args:
            policy: page break policy
        """
        self.setPageBreakPolicy(gui.textformat.PAGE_BREAK_FLAG.get_enum_value(policy))

    def get_page_break_policy(self) -> gui.textformat.PageBreakFlagStr:
        """Get the current page break policy.

        Returns:
            page break policy
        """
        return gui.textformat.PAGE_BREAK_FLAG.inverse[self.pageBreakPolicy()]
