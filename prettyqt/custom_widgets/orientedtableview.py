from __future__ import annotations

import logging

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


class OrientedTableView(widgets.TableView):
    """TableView class with some convenience methods for oriented tables."""

    def __init__(self, orientation: constants.Orientation, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.orientation = orientation

    def get_higher_levels(self, levels):
        model = self.model()
        if self.is_horizontal():
            # Get the header's selected columns
            # Removes the higher levels so that only the lowest level of the header
            # affects the data table selection
            return core.ItemSelection(
                model.index(0, 0), model.index(levels - 2, model.columnCount() - 1)
            )
        else:
            return core.ItemSelection(
                model.index(0, 0), model.index(model.rowCount() - 1, levels - 2)
            )

    def set_section_span(self, row, column, count):
        if self.is_horizontal():
            self.setSpan(row, column, 1, count)
        else:
            self.setSpan(column, row, count, 1)

    def sectionAt(self, val: int):
        return self.columnAt(val) if self.is_horizontal() else self.rowAt(val)

    def over_header_edge(self, position: int, margin: int = 3):
        # Return the index of the column this x position is on the right edge of
        left = self.sectionAt(position - margin)
        right = self.sectionAt(position + margin)
        if left != right != 0:
            # We're at the left edge of the first column
            return left

    def is_horizontal(self) -> bool:
        return self.orientation == constants.HORIZONTAL

    def sectionWidth(self, val: int):
        return self.columnWidth(val) if self.is_horizontal() else self.rowHeight(val)

    def setSectionWidth(self, val: int, val2):
        if self.is_horizontal():
            self.setColumnWidth(val, val2)
        else:
            self.setRowHeight(val, val2)

    def get_split_cursor(self):
        if self.is_horizontal():
            return gui.Cursor(QtCore.Qt.CursorShape.SplitHCursor)
        else:
            return gui.Cursor(QtCore.Qt.CursorShape.SplitVCursor)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    with app.debug_mode():
        app.set_style("fusion")
        view = OrientedTableView()
        view.show()
        app.main_loop()
