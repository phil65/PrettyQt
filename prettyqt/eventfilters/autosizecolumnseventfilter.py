from __future__ import annotations

from prettyqt import core, eventfilters, widgets


class AutoSizeColumnsEventFilter(eventfilters.BaseEventFilter):
    ID = "autosize_columns"

    def __init__(self, parent: widgets.TableView | widgets.TreeView):
        super().__init__(parent)
        self._widget = parent
        parent.h_scrollbar.valueChanged.connect(self._on_scroll)
        parent.model_changed.connect(self._on_model_change)
        self.autosized_cols = set()

    def _on_model_change(self):
        self.autosized_cols = set()

    def eventFilter(self, obj, event: core.Event) -> bool:
        match event.type():
            case core.Event.Type.Resize:
                self._on_scroll()
                return False
        return super().eventFilter(obj, event)

    def _on_scroll(self):
        colcount = self._widget.model().columnCount()
        col, end = self._widget.get_visible_section_span("horizontal")
        width = self._widget.viewport().width()
        while col <= end:
            if col not in self.autosized_cols:
                self.autosized_cols.add(col)
                self._widget.resizeColumnToContents(col)
            col += 1
            end = self._widget.columnAt(width)
            end = colcount if end == -1 else end


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    widget = debugging.example_table()
    widget.set_delegate("variant")
    test = AutoSizeColumnsEventFilter(widget)
    widget.installEventFilter(test)
    widget.show()
    app.main_loop()
