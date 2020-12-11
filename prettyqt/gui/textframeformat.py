from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError


POSITIONS = bidict(
    in_flow=QtGui.QTextFrameFormat.InFlow,
    flow_left=QtGui.QTextFrameFormat.FloatLeft,
    flow_right=QtGui.QTextFrameFormat.FloatRight,
)

BORDER_STYLES = bidict(
    none=QtGui.QTextFrameFormat.BorderStyle_None,
    dotted=QtGui.QTextFrameFormat.BorderStyle_Dotted,
    dashed=QtGui.QTextFrameFormat.BorderStyle_Dashed,
    solid=QtGui.QTextFrameFormat.BorderStyle_Solid,
    double=QtGui.QTextFrameFormat.BorderStyle_Double,
    dot_dash=QtGui.QTextFrameFormat.BorderStyle_DotDash,
    dot_dot_dash=QtGui.QTextFrameFormat.BorderStyle_DotDotDash,
    groove=QtGui.QTextFrameFormat.BorderStyle_Groove,
    ridge=QtGui.QTextFrameFormat.BorderStyle_Ridge,
    inset=QtGui.QTextFrameFormat.BorderStyle_Inset,
    outset=QtGui.QTextFrameFormat.BorderStyle_Outset,
)


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

    def set_border_style(self, style: str):
        """Set border style.

        Valid values: "none", "dotted", "dashed", "solid", "double", "dot_dash",
                      "dot_dot_dash", "groove", "ridge", "inset", "outset"

        Args:
            style: border style

        Raises:
            InvalidParamError: border style does not exist
        """
        if style not in BORDER_STYLES:
            raise InvalidParamError(style, BORDER_STYLES)
        self.setBorderStyle(BORDER_STYLES[style])

    def get_border_style(self) -> str:
        """Get the current border style.

        Possible values: "none", "dotted", "dashed", "solid", "double", "dot_dash",
                             "dot_dot_dash", "groove", "ridge", "inset", "outset"

        Returns:
            border style
        """
        return BORDER_STYLES.inverse[self.borderStyle()]

    def set_page_break_policy(self, policy: str):
        """Set page break policy.

        Valid values: "auto", "always_before", "always_after"

        Args:
            policy: page break policy

        Raises:
            InvalidParamError: page break policy does not exist
        """
        if policy not in gui.textformat.PAGE_BREAK_FLAG:
            raise InvalidParamError(policy, gui.textformat.PAGE_BREAK_FLAG)
        self.setPageBreakPolicy(gui.textformat.PAGE_BREAK_FLAG[policy])

    def get_page_break_policy(self) -> str:
        """Get the current page break policy.

        Possible values: "auto", "always_before", "always_after"

        Returns:
            page break policy
        """
        return gui.textformat.PAGE_BREAK_FLAG.inverse[self.pageBreakPolicy()]

    def set_position(self, position: str):
        """Set position.

        Valid values: "in_flow", "flow_left", "flow_right"

        Args:
            position: position

        Raises:
            InvalidParamError: position does not exist
        """
        if position not in POSITIONS:
            raise InvalidParamError(position, POSITIONS)
        self.setPosition(POSITIONS[position])

    def get_position(self) -> str:
        """Get the current position.

        Possible values: "in_flow", "flow_left", "flow_right"

        Returns:
            position
        """
        return POSITIONS.inverse[self.position()]
