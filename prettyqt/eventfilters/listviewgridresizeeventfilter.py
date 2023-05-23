from __future__ import annotations

from prettyqt import core, eventfilters
from prettyqt.qt import QtCore


class ListViewGridResizeEventFilter(eventfilters.BaseEventFilter):
    """Eventfilter that scales grid size of ListViews."""

    def __init__(self, num_columns=5, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self._view_columns = num_columns

    def eventFilter(self, source, event: core.Event) -> bool:
        match event.type():
            case core.Event.Type.Resize:
                self._resize(source)
        return super().eventFilter(source, event)

    def _resize(self, source):
        width = source.width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tile_width = int(width / self._view_columns)
        icon_width = int(tile_width * 0.8)
        source.setGridSize(QtCore.QSize(tile_width, tile_width))
        source.setIconSize(QtCore.QSize(icon_width, icon_width))


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.ListView()
    # widget.set_icon("mdi.folder")
    test = ListViewGridResizeEventFilter(parent=widget)
    widget.installEventFilter(test)
    widget.show()
    app.main_loop()
