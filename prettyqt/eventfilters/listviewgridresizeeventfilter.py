from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core, eventfilters


if TYPE_CHECKING:
    from prettyqt import widgets


class ListViewGridResizeEventFilter(eventfilters.BaseEventFilter):
    """Eventfilter that scales grid size of ListViews."""

    ID = "listview_grid_resize"

    def __init__(
        self, num_columns: int = 5, parent: widgets.ListView | None = None, **kwargs
    ):
        super().__init__(parent=parent, **kwargs)
        self._view_columns = num_columns

    def eventFilter(self, source, event: core.Event) -> bool:
        match event.type():
            case core.Event.Type.Resize:
                self._resize(source)
        return super().eventFilter(source, event)

    def _resize(self, source: widgets.ListView):
        width = source.width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tile_width = int(width / self._view_columns)
        icon_width = int(tile_width * 0.8)
        source.setGridSize(core.QSize(tile_width, tile_width))
        source.setIconSize(core.QSize(icon_width, icon_width))


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.ListView()
    # widget.set_icon("mdi.folder")
    test = ListViewGridResizeEventFilter(parent=widget)
    widget.installEventFilter(test)
    widget.show()
    app.exec()
