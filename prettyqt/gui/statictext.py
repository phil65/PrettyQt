from __future__ import annotations

from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, get_repr


PERFORMANCE_HINT = bidict(
    moderate=QtGui.QStaticText.PerformanceHint.ModerateCaching,
    aggressive=QtGui.QStaticText.PerformanceHint.AggressiveCaching,
)

PerformanceHintStr = Literal["moderate", "aggressive"]


class StaticText(QtGui.QStaticText):
    def __repr__(self):
        return get_repr(self, self.text())

    def __str__(self):
        return self.text()

    def get_size(self) -> core.SizeF:
        return core.SizeF(self.size())

    def set_text_format(self, text_format: constants.TextFormatStr):
        """Set the text format.

        Allowed values are "rich", "plain", "auto", "markdown"

        Args:
            text_format: text format to use

        Raises:
            InvalidParamError: text format does not exist
        """
        if text_format not in constants.TEXT_FORMAT:
            raise InvalidParamError(text_format, constants.TEXT_FORMAT)
        self.setTextFormat(constants.TEXT_FORMAT[text_format])

    def get_text_format(self) -> constants.TextFormatStr:
        """Return current text format.

        Possible values: "rich", "plain", "auto", "markdown"

        Returns:
            text format
        """
        return constants.TEXT_FORMAT.inverse[self.textFormat()]

    def set_performance_hint(self, hint: PerformanceHintStr):
        """Set the performance hint.

        Args:
            hint: performance hint to use

        Raises:
            InvalidParamError: performance hint does not exist
        """
        if hint not in PERFORMANCE_HINT:
            raise InvalidParamError(hint, PERFORMANCE_HINT)
        self.setPerformanceHint(PERFORMANCE_HINT[hint])

    def get_performance_hint(self) -> PerformanceHintStr:
        """Return current performance hint.

        Returns:
            performance hint
        """
        return PERFORMANCE_HINT.inverse[self.performanceHint()]


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    text = StaticText()
    text.get_size()
