from __future__ import annotations

import logging

from prettyqt import constants, core, gui, widgets


logger = logging.getLogger(__name__)


class OrientedTableView(widgets.TableView):
    """TableView class with some convenience methods for oriented tables."""

    def __init__(
        self, orientation: constants.Orientation | constants.OrientationStr, **kwargs
    ):
        super().__init__(**kwargs)
        self.orientation = constants.ORIENTATION.get_enum_value(orientation)

    @classmethod
    def setup_example(cls):
        return cls(orientation="vertical")

    def get_higher_levels(self, levels: int) -> core.ItemSelection:
        model = self.model()
        if self.is_horizontal():
            # Get the header's selected columns
            # Removes the higher levels so that only the lowest level of the header
            # affects the data table selection
            return core.ItemSelection(
                model.index(0, 0), model.index(levels - 2, model.columnCount() - 1)
            )
        return core.ItemSelection(
            model.index(0, 0), model.index(model.rowCount() - 1, levels - 2)
        )

    def set_section_span(self, row: int, column: int, count: int):
        if self.is_horizontal():
            self.setSpan(row, column, 1, count)
        else:
            self.setSpan(column, row, count, 1)

    def sectionAt(self, val: int):
        return self.columnAt(val) if self.is_horizontal() else self.rowAt(val)

    def over_header_edge(self, position: int, margin: int = 3) -> int:
        # Return the index of the column this x position is on the right edge of
        left = self.sectionAt(position - margin)
        right = self.sectionAt(position + margin)
        if left != right != 0:
            # We're at the left edge of the first column
            return left
        return None

    def is_horizontal(self) -> bool:
        return self.orientation == constants.HORIZONTAL

    def sectionWidth(self, val: int):
        return self.columnWidth(val) if self.is_horizontal() else self.rowHeight(val)

    def setSectionWidth(self, section: int, width: int):
        if self.is_horizontal():
            self.setColumnWidth(section, width)
        else:
            self.setRowHeight(section, width)

    def get_split_cursor(self) -> gui.Cursor:
        if self.is_horizontal():
            return gui.Cursor(constants.CursorShape.SplitHCursor)
        return gui.Cursor(constants.CursorShape.SplitVCursor)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    with app.debug_mode():
        app.set_style("fusion")
        view = OrientedTableView()
        view.show()
        app.exec()
