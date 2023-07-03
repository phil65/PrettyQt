from __future__ import annotations

from prettyqt import constants, core, eventfilters, widgets


class AutoSizeColumnsEventFilter(eventfilters.BaseEventFilter):
    ID = "autosize_columns"

    def __init__(
        self,
        parent: widgets.TableView | widgets.TreeView,
        orientation: constants.Orientation
        | constants.OrientationStr = constants.VERTICAL,
    ):
        super().__init__(parent)
        self._widget = parent
        self.orientation = constants.ORIENTATION.get_enum_value(orientation)
        parent.model_changed.connect(self._on_model_change)
        self._autosized_sections = set()
        self.last_span: tuple[int, int] | None = None

        if self.orientation == constants.VERTICAL:
            parent.h_scrollbar.valueChanged.connect(self._on_scroll)
        else:
            parent.v_scrollbar.valueChanged.connect(self._on_scroll)
        # if sel_model := parent.selectionModel():
        #     sel_model.currentColumnChanged.connect(self._resize_current_col_to_content)

    def _on_model_change(self):
        self._autosized_sections = set()
        # sel_model = self._widget.selectionModel()
        # sel_model.currentColumnChanged.connect(self._resize_current_col_to_content)

    def eventFilter(self, obj, event: core.Event) -> bool:
        match event.type():
            case core.Event.Type.Resize:
                self._on_scroll()
                return False
        return super().eventFilter(obj, event)

    # def _resize_current_col_to_content(self, new_index, old_index):
    #     if new_index.column() not in self._autosized_sections:
    #         # ensure the requested column is fully into view after resizing
    #         self._widget.resize_visible_columns_to_contents()
    #         self._widget.scrollTo(new_index)

    def _on_scroll(self):
        if self.orientation == constants.VERTICAL:
            colcount = self._widget.model().columnCount()
            span = self._widget.get_visible_section_span("horizontal")
            if span == self.last_span:
                return
            self.last_span = span
            col, end = span
            width = self._widget.viewport().width()
            while col <= end:
                if col not in self._autosized_sections:
                    self._autosized_sections.add(col)
                    self._widget.resizeColumnToContents(col)
                col += 1
                end = self._widget.columnAt(width)
                end = colcount if end == -1 else end
        else:
            rowcount = self._widget.model().rowCount()
            span = self._widget.get_visible_section_span("vertical")
            if span == self.last_span:
                return
            self.last_span = span
            row, end = span
            height = self._widget.viewport().height()
            while row <= end:
                if row not in self._autosized_sections:
                    self._autosized_sections.add(row)
                    self._widget.resizeRowToContents(row)
                row += 1
                end = self._widget.rowAt(height)
                end = rowcount if end == -1 else end


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    widget = debugging.example_table()
    widget.set_delegate("editor")
    test = AutoSizeColumnsEventFilter(widget)
    widget.installEventFilter(test)
    widget.show()
    app.exec()
