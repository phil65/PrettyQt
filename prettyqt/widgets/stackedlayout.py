from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict


StackingModeStr = Literal["one", "all"]

STACKING_MODE: bidict[StackingModeStr, widgets.QStackedLayout.StackingMode] = bidict(
    one=widgets.QStackedLayout.StackingMode.StackOne,
    all=widgets.QStackedLayout.StackingMode.StackAll,
)


class StackedLayout(widgets.LayoutMixin, widgets.QStackedLayout):
    """Layout containing stack of widgets where only one widget is visible at a time."""

    ID = "stacked"

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"stackingMode": STACKING_MODE}
        return maps

    def set_stacking_mode(self, mode: StackingModeStr):
        self.setStackingMode(STACKING_MODE[mode])

    def get_stacking_mode(self) -> StackingModeStr:
        return STACKING_MODE.inverse[self.stackingMode()]

    def __add__(self, other: widgets.QWidget | widgets.QLayout):
        self.add(other)
        return self

    def set_current_widget(self, widget: widgets.QWidget):
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
    app.exec()
