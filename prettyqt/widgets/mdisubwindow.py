from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import bidict


SUB_WINDOW_OPTION = bidict(
    rubber_band_resize=widgets.QMdiSubWindow.SubWindowOption.RubberBandResize,
    rubber_band_move=widgets.QMdiSubWindow.SubWindowOption.RubberBandMove,
)


class MdiSubWindow(widgets.WidgetMixin, widgets.QMdiSubWindow):
    def serialize_fields(self):
        return dict(
            keyboard_single_step=self.keyboardSingleStep(),
            keyboard_page_step=self.keyboardPageStep(),
        )


if __name__ == "__main__":
    app = widgets.app()
    widget = MdiSubWindow()
    widget.show()
    app.exec()
