from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError


QtGui.QTextTableCellFormat.__bases__ = (gui.TextCharFormat,)


class TextTableCellFormat(QtGui.QTextTableCellFormat):
    def get_bottom_border_brush(self) -> gui.Brush:
        return gui.Brush(self.bottomBorderBrush())

    def set_border_style(self, style: gui.textframeformat.BorderStyleStr):
        """Set border style.

        Args:
            style: border style

        Raises:
            InvalidParamError: border style does not exist
        """
        if style not in gui.textframeformat.BORDER_STYLES:
            raise InvalidParamError(style, gui.textframeformat.BORDER_STYLES)
        self.setBorderStyle(gui.textframeformat.BORDER_STYLES[style])

    def set_bottom_border_style(self, style: gui.textframeformat.BorderStyleStr):
        """Set bottom border style.

        Args:
            style: bottom border style

        Raises:
            InvalidParamError: bottom border style does not exist
        """
        if style not in gui.textframeformat.BORDER_STYLES:
            raise InvalidParamError(style, gui.textframeformat.BORDER_STYLES)
        self.setBottomBorderStyle(gui.textframeformat.BORDER_STYLES[style])

    def get_bottom_border_style(self) -> gui.textframeformat.BorderStyleStr:
        """Get the current bottom border style.

        Returns:
            bottom border style
        """
        return gui.textframeformat.BORDER_STYLES.inverse[self.bottomBorderStyle()]

    def get_left_border_brush(self) -> gui.Brush:
        return gui.Brush(self.leftBorderBrush())

    def set_left_border_style(self, style: gui.textframeformat.BorderStyleStr):
        """Set left border style.

        Args:
            style: left border style

        Raises:
            InvalidParamError: left border style does not exist
        """
        if style not in gui.textframeformat.BORDER_STYLES:
            raise InvalidParamError(style, gui.textframeformat.BORDER_STYLES)
        self.setLeftBorderStyle(gui.textframeformat.BORDER_STYLES[style])

    def get_left_border_style(self) -> gui.textframeformat.BorderStyleStr:
        """Get the current left border style.

        Returns:
            left border style
        """
        return gui.textframeformat.BORDER_STYLES.inverse[self.leftBorderStyle()]

    def get_right_border_brush(self) -> gui.Brush:
        return gui.Brush(self.rightBorderBrush())

    def set_right_border_style(self, style: gui.textframeformat.BorderStyleStr):
        """Set right border style.

        Args:
            style: right border style

        Raises:
            InvalidParamError: right border style does not exist
        """
        if style not in gui.textframeformat.BORDER_STYLES:
            raise InvalidParamError(style, gui.textframeformat.BORDER_STYLES)
        self.setRightBorderStyle(gui.textframeformat.BORDER_STYLES[style])

    def get_right_border_style(self) -> gui.textframeformat.BorderStyleStr:
        """Get the current right border style.

        Returns:
            right border style
        """
        return gui.textframeformat.BORDER_STYLES.inverse[self.rightBorderStyle()]

    def get_top_border_brush(self) -> gui.Brush:
        return gui.Brush(self.topBorderBrush())

    def set_top_border_style(self, style: gui.textframeformat.BorderStyleStr):
        """Set top border style.

        Args:
            style: top border style

        Raises:
            InvalidParamError: top border style does not exist
        """
        if style not in gui.textframeformat.BORDER_STYLES:
            raise InvalidParamError(style, gui.textframeformat.BORDER_STYLES)
        self.setTopBorderStyle(gui.textframeformat.BORDER_STYLES[style])

    def get_top_border_style(self) -> gui.textframeformat.BorderStyleStr:
        """Get the current top border style.

        Returns:
            top border style
        """
        return gui.textframeformat.BORDER_STYLES.inverse[self.topBorderStyle()]


if __name__ == "__main__":
    fmt = TextTableCellFormat()
    print(bool(fmt))
