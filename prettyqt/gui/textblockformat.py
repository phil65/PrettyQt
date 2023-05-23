from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


LINE_HEIGHT_TYPES = bidict(
    single=QtGui.QTextBlockFormat.LineHeightTypes.SingleHeight,
    proportional=QtGui.QTextBlockFormat.LineHeightTypes.ProportionalHeight,
    fixed=QtGui.QTextBlockFormat.LineHeightTypes.FixedHeight,
    minimum=QtGui.QTextBlockFormat.LineHeightTypes.MinimumHeight,
    line_distance=QtGui.QTextBlockFormat.LineHeightTypes.LineDistanceHeight,
)

LineHeightTypeStr = Literal[
    "single",
    "proportional",
    "fixed",
    "minimum",
    "line_distance",
]

MARKER_TYPE = bidict(
    none=QtGui.QTextBlockFormat.MarkerType.NoMarker,
    unchecked=QtGui.QTextBlockFormat.MarkerType.Unchecked,
    checked=QtGui.QTextBlockFormat.MarkerType.Checked,
)

MarkerTypeStr = Literal[
    "none",
    "unchecked",
    "checked",
]


class TextBlockFormat(gui.TextFormatMixin, QtGui.QTextBlockFormat):
    def set_marker(self, marker: MarkerTypeStr):
        """Set the marker.

        Args:
            marker: marker

        Raises:
            InvalidParamError: invalid marker
        """
        if marker not in MARKER_TYPE:
            raise InvalidParamError(marker, MARKER_TYPE)
        self.setMarker(MARKER_TYPE[marker])

    def get_marker(self) -> MarkerTypeStr:
        """Get current marker.

        Returns:
            current marker
        """
        return MARKER_TYPE.inverse[self.marker()]

    def set_alignment(self, alignment: constants.AlignmentStr):
        """Set the alignment of the format.

        Args:
            alignment: alignment for the format

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        self.setAlignment(constants.ALIGNMENTS[alignment])

    def get_alignment(self) -> constants.AlignmentStr:
        """Return current alignment.

        Returns:
            alignment
        """
        return constants.ALIGNMENTS.inverse[self.alignment()]

    def set_page_break_policy(self, policy: gui.textformat.PageBreakFlagStr):
        """Set page break policy.

        Args:
            policy: page break policy

        Raises:
            InvalidParamError: page break policy does not exist
        """
        if policy not in gui.textformat.PAGE_BREAK_FLAG:
            raise InvalidParamError(policy, gui.textformat.PAGE_BREAK_FLAG)
        self.setPageBreakPolicy(gui.textformat.PAGE_BREAK_FLAG[policy])

    def get_page_break_policy(self) -> gui.textformat.PageBreakFlagStr:
        """Get the current page break policy.

        Returns:
            page break policy
        """
        return gui.textformat.PAGE_BREAK_FLAG.inverse[self.pageBreakPolicy()]