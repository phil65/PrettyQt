from __future__ import annotations

from typing import overload

from prettyqt import animations, widgets
from prettyqt.utils import listdelegators


class StackedWidget(widgets.FrameMixin, widgets.QStackedWidget):
    """Widget containing stack of widgets where only one widget is visible at a time."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animator = animations.Animator(self)

    def __add__(self, other: widgets.QWidget) -> StackedWidget:
        self.addWidget(other)
        return self

    @overload
    def __getitem__(self, index: int) -> widgets.QWidget:
        ...

    @overload
    def __getitem__(self, index: slice) -> listdelegators.ListDelegator[widgets.QWidget]:
        ...

    def __getitem__(
        self, index: int | slice
    ) -> widgets.QWidget | listdelegators.ListDelegator[widgets.QWidget]:
        match index:
            case int():
                if index >= self.count():
                    raise IndexError(index)
                return self.widget(index)
            case slice():
                rng = range(index.start or 0, index.stop or self.count(), index.step or 1)
                return listdelegators.ListDelegator(self.widget(i) for i in rng)
            case _:
                raise TypeError(index)

    def __delitem__(self, item: int | widgets.QWidget):
        if isinstance(item, int):
            item = self.widget(item)
        self.removeWidget(item)

    def __len__(self):
        # needed for PySide6
        return self.count()

    def __contains__(self, item: widgets.QWidget):
        return self.indexOf(item) >= 0

    # __iter__ not needed, we have __getitem__ and __len__


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    stackedwidget = StackedWidget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.PlainTextEdit("Test 243434")
    stackedwidget += widget2
    stackedwidget += widget3
    for i in stackedwidget:
        print(i)
    stackedwidget.show()
    app.exec()
