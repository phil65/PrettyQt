from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


QtWidgets.QMdiSubWindow.__bases__ = (widgets.Widget,)


SUB_WINDOW_OPTION = bidict(
    rubber_band_resize=QtWidgets.QMdiSubWindow.SubWindowOption.RubberBandResize,
    rubber_band_move=QtWidgets.QMdiSubWindow.SubWindowOption.RubberBandMove,
)


class MdiSubWindow(QtWidgets.QMdiSubWindow):
    def serialize_fields(self):
        return dict(
            keyboard_single_step=self.keyboardSingleStep(),
            keyboard_page_step=self.keyboardPageStep(),
        )


if __name__ == "__main__":
    app = widgets.app()
    widget = MdiSubWindow()
    widget.show()
    app.main_loop()
