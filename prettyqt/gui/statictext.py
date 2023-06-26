from __future__ import annotations

from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr


PerformanceHintStr = Literal["moderate", "aggressive"]

PERFORMANCE_HINT: bidict[PerformanceHintStr, QtGui.QStaticText.PerformanceHint] = bidict(
    moderate=QtGui.QStaticText.PerformanceHint.ModerateCaching,
    aggressive=QtGui.QStaticText.PerformanceHint.AggressiveCaching,
)


class StaticText(QtGui.QStaticText):
    def __repr__(self):
        return get_repr(self, self.text())

    def __str__(self):
        return self.text()

    def get_size(self) -> core.SizeF:
        return core.SizeF(self.size())

    def set_text_format(
        self, text_format: constants.TextFormatStr | constants.TextFormat
    ):
        """Set the text format.

        Allowed values are "rich", "plain", "auto", "markdown"

        Args:
            text_format: text format to use
        """
        self.setTextFormat(constants.TEXT_FORMAT.get_enum_value(text_format))

    def get_text_format(self) -> constants.TextFormatStr:
        """Return current text format.

        Possible values: "rich", "plain", "auto", "markdown"

        Returns:
            text format
        """
        return constants.TEXT_FORMAT.inverse[self.textFormat()]

    def set_performance_hint(
        self, hint: PerformanceHintStr | QtGui.QStaticText.PerformanceHint
    ):
        """Set the performance hint.

        Args:
            hint: performance hint to use
        """
        self.setPerformanceHint(PERFORMANCE_HINT.get_enum_value(hint))

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
