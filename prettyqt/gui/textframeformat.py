from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


POSITIONS = bidict(
    in_flow=QtGui.QTextFrameFormat.Position.InFlow,
    flow_left=QtGui.QTextFrameFormat.Position.FloatLeft,
    flow_right=QtGui.QTextFrameFormat.Position.FloatRight,
)

PositionStr = Literal["in_flow", "flow_right", "flow_left"]

BORDER_STYLES = bidict(
    none=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_None,
    dotted=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Dotted,
    dashed=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Dashed,
    solid=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Solid,
    double=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Double,
    dot_dash=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_DotDash,
    dot_dot_dash=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_DotDotDash,
    groove=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Groove,
    ridge=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Ridge,
    inset=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Inset,
    outset=QtGui.QTextFrameFormat.BorderStyle.BorderStyle_Outset,
)

BorderStyleStr = Literal[
    "none",
    "dotted",
    "dashed",
    "solid",
    "double",
    "dot_dash",
    "dot_dot_dash",
    "groove",
    "ridge",
    "inset",
    "outset",
]


QtGui.QTextFrameFormat.__bases__ = (gui.TextFormat,)


class TextFrameFormat(QtGui.QTextFrameFormat):
    def get_height(self) -> gui.TextLength:
        length = self.height()
        return gui.TextLength(length.type(), length.rawValue())

    def get_width(self) -> gui.TextLength:
        length = self.width()
        return gui.TextLength(length.type(), length.rawValue())

    def get_border_brush(self) -> gui.Brush:
        return gui.Brush(self.borderBrush())

    def set_border_style(self, style: BorderStyleStr):
        """Set border style.

        Args:
            style: border style

        Raises:
            InvalidParamError: border style does not exist
        """
        if style not in BORDER_STYLES:
            raise InvalidParamError(style, BORDER_STYLES)
        self.setBorderStyle(BORDER_STYLES[style])

    def get_border_style(self) -> BorderStyleStr:
        """Get the current border style.

        Returns:
            border style
        """
        return BORDER_STYLES.inverse[self.borderStyle()]

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

    def set_position(self, position: PositionStr):
        """Set position.

        Args:
            position: position

        Raises:
            InvalidParamError: position does not exist
        """
        if position not in POSITIONS:
            raise InvalidParamError(position, POSITIONS)
        self.setPosition(POSITIONS[position])

    def get_position(self) -> PositionStr:
        """Get the current position.

        Returns:
            position
        """
        return POSITIONS.inverse[self.position()]
