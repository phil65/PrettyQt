from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


STACKING_MODE = bidict(
    one=QtWidgets.QStackedLayout.StackingMode.StackOne,
    all=QtWidgets.QStackedLayout.StackingMode.StackAll,
)

StackingModeStr = Literal["one", "all"]


class StackedLayout(widgets.LayoutMixin, QtWidgets.QStackedLayout):
    ID = "stacked"

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"stackingMode": STACKING_MODE}
        return maps

    def set_stacking_mode(self, mode: StackingModeStr):
        self.setStackingMode(STACKING_MODE[mode])

    def get_stacking_mode(self) -> StackingModeStr:
        return STACKING_MODE.inverse[self.stackingMode()]

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout):
        self.add(other)
        return self

    def set_current_widget(self, widget: QtWidgets.QWidget):
        self.setCurrentWidget(widget)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    layout = StackedLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.RadioButton("Test 2")
    layout += widget2
    layout += widget3
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
