from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui
from prettyqt.utils import bidict


LineHeightTypeStr = Literal[
    "single",
    "proportional",
    "fixed",
    "minimum",
    "line_distance",
]

LINE_HEIGHT_TYPES: bidict[MarkerTypeStr, gui.QTextBlockFormat.LineHeightTypes] = bidict(
    single=gui.QTextBlockFormat.LineHeightTypes.SingleHeight,
    proportional=gui.QTextBlockFormat.LineHeightTypes.ProportionalHeight,
    fixed=gui.QTextBlockFormat.LineHeightTypes.FixedHeight,
    minimum=gui.QTextBlockFormat.LineHeightTypes.MinimumHeight,
    line_distance=gui.QTextBlockFormat.LineHeightTypes.LineDistanceHeight,
)

MarkerTypeStr = Literal[
    "none",
    "unchecked",
    "checked",
]

MARKER_TYPE: bidict[MarkerTypeStr, gui.QTextBlockFormat.MarkerType] = bidict(
    none=gui.QTextBlockFormat.MarkerType.NoMarker,
    unchecked=gui.QTextBlockFormat.MarkerType.Unchecked,
    checked=gui.QTextBlockFormat.MarkerType.Checked,
)


class TextBlockFormat(gui.TextFormatMixin, gui.QTextBlockFormat):
    def set_marker(self, marker: MarkerTypeStr | gui.QTextBlockFormat.MarkerType):
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
