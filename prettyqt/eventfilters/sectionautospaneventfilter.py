from __future__ import annotations

from prettyqt import constants, core, eventfilters, widgets


class SectionAutoSpanEventFilter(eventfilters.BaseEventFilter):
    ID = "autospan_sections"

    def __init__(
        self,
        parent: widgets.TableView | widgets.TreeView,
        orientation=constants.HORIZONTAL,
    ):
        super().__init__(parent)
        self._widget = parent
        self._last_start = None
        self._last_end = None
        self.orientation = orientation
        if orientation == constants.HORIZONTAL:
            parent.h_scrollbar.valueChanged.connect(self._update_spans)
        else:
            parent.v_scrollbar.valueChanged.connect(self._update_spans)
        parent.model().headerDataChanged.connect(self._on_force_update)
        parent.model_changed.connect(self._on_force_update)
        parent.installEventFilter(self)
        self._update_spans()
        # sel_model = parent.selectionModel()
        # if not sel_model:
        #     return

    def _on_force_update(self):
        self._update_spans(True)

    def eventFilter(self, obj, event: core.Event) -> bool:
        match event.type():
            case core.Event.Type.Resize:
                self._update_spans()
                return False
        return super().eventFilter(obj, event)

    def _update_spans(self, force: bool = False):
        cols = self._widget.get_visible_section_span("horizontal", margin=1)
        rows = self._widget.get_visible_section_span("vertical", margin=1)
        start = (rows[0], cols[0])
        end = (rows[1], cols[1])
        if start == self._last_start and end == self._last_end and not force:
            return
        self._last_start = start
        self._last_end = end
        self._widget.clearSpans()
        self._widget.auto_span(orientation=self.orientation, start=start, end=end)


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    widget = debugging.example_table()
    widget.set_delegate("variant")
    with app.debug_mode():
        test = SectionAutoSpanEventFilter(widget)
        widget.show()
        app.main_loop()
