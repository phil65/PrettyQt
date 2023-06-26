from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import bidict


FontFilterStr = Literal["all", "scalable", "non_scalable", "monospaced", "proportional"]

FONT_FILTERS: bidict[FontFilterStr, QtWidgets.QFontComboBox.FontFilter] = bidict(
    all=QtWidgets.QFontComboBox.FontFilter.AllFonts,
    scalable=QtWidgets.QFontComboBox.FontFilter.ScalableFonts,
    non_scalable=QtWidgets.QFontComboBox.FontFilter.NonScalableFonts,
    monospaced=QtWidgets.QFontComboBox.FontFilter.MonospacedFonts,
    proportional=QtWidgets.QFontComboBox.FontFilter.ProportionalFonts,
)


class FontComboBox(widgets.ComboBoxMixin, QtWidgets.QFontComboBox):
    value_changed = core.Signal(gui.QFont)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "fontFilters": FONT_FILTERS,
            "writingSystem": gui.fontdatabase.WRITING_SYSTEM,
        }
        return maps

    def set_font_filters(self, *filters: FontFilterStr):
        """Set font filters.

        Args:
            filters: font filters to use
        """
        if not filters:
            filters = ("all",)
        flags = FONT_FILTERS.merge_flags(filters)
        self.setFontFilters(flags)

    def get_font_filters(self) -> list[FontFilterStr]:
        """Return list of font filters.

        Returns:
            font filter list
        """
        return FONT_FILTERS.get_list(self.fontFilters())

    def set_value(self, value: QtGui.QFont):
        self.setCurrentFont(value)

    def get_value(self) -> gui.QFont:
        return gui.QFont(self.get_current_font())

    def get_current_font(self) -> gui.Font:
        return gui.Font(self.currentFont())

    # without this, the user property would be currentText, which is not what we want.
    # PyQt6 doesnt like gui.Font here.
    value = core.Property(QtGui.QFont, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = FontComboBox()
    widget.set_value(gui.Font("Script"))
    widget.show()
    app.exec()
