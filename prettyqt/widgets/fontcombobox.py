from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, helpers


FONT_FILTERS = bidict(
    all=QtWidgets.QFontComboBox.FontFilter.AllFonts,
    scalable=QtWidgets.QFontComboBox.FontFilter.ScalableFonts,
    non_scalable=QtWidgets.QFontComboBox.FontFilter.NonScalableFonts,
    monospaced=QtWidgets.QFontComboBox.FontFilter.MonospacedFonts,
    proportional=QtWidgets.QFontComboBox.FontFilter.ProportionalFonts,
)

FontFilterStr = Literal["all", "scalable", "non_scalable", "monospaced", "proportional"]


class FontComboBox(widgets.ComboBoxMixin, QtWidgets.QFontComboBox):
    value_changed = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentIndexChanged.connect(self.index_changed)

    def set_font_filters(self, *filters: FontFilterStr):
        """Set font filters.

        Args:
            filters: font filters to use

        Raises:
            InvalidParamError: invalid font filters
        """
        if not filters:
            filters = ("all",)
        for item in filters:
            if item not in FONT_FILTERS:
                raise InvalidParamError(item, FONT_FILTERS)
        flags = helpers.merge_flags(filters, FONT_FILTERS)
        self.setFontFilters(flags)

    def get_font_filters(self) -> list[FontFilterStr]:
        """Return list of font filters.

        Returns:
            font filter list
        """
        return FONT_FILTERS.get_list(self.fontFilters())

    def set_value(self, value: QtGui.QFont):
        self.setCurrentFont(value)

    def get_value(self) -> gui.Font:
        return self.get_current_font()

    def get_current_font(self) -> gui.Font:
        return gui.Font(self.currentFont())


if __name__ == "__main__":
    app = widgets.app()
    widget = FontComboBox()
    widget.value_changed.connect(print)
    widget.set_value(gui.Font("Script"))
    widget.show()
    app.main_loop()
