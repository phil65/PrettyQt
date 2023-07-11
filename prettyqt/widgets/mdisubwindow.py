from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import bidict


SUB_WINDOW_OPTION = bidict(
    rubber_band_resize=widgets.QMdiSubWindow.SubWindowOption.RubberBandResize,
    rubber_band_move=widgets.QMdiSubWindow.SubWindowOption.RubberBandMove,
)


class MdiSubWindow(widgets.WidgetMixin, widgets.QMdiSubWindow):
    """Subwindow class for QMdiArea."""


if __name__ == "__main__":
    app = widgets.app()
    widget = MdiSubWindow()
    widget.show()
    app.exec()
