from __future__ import annotations

from typing import overload

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import animator, listdelegators


class StackedWidget(widgets.FrameMixin, QtWidgets.QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animator = animator.Animator(self)

    def __add__(self, other: QtWidgets.QWidget) -> StackedWidget:
        self.addWidget(other)
        return self

    @overload
    def __getitem__(self, index: int) -> QtWidgets.QWidget:
        ...

    @overload
    def __getitem__(
        self, index: slice
    ) -> listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        ...

    def __getitem__(
        self, index: int | slice
    ) -> QtWidgets.QWidget | listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        match index:
            case int():
                if index >= self.count():
                    raise IndexError(index)
                return self.widget(index)
            case slice():
                rng = range(index.start or 0, index.stop or self.count(), index.step or 1)
                return listdelegators.BaseListDelegator(self.widget(i) for i in rng)
            case _:
                raise TypeError(index)

    def __delitem__(self, item: int | QtWidgets.QWidget):
        if isinstance(item, int):
            item = self.widget(item)
        self.removeWidget(item)

    def __len__(self):
        # needed for PySide6
        return self.count()

    def __contains__(self, item: QtWidgets.QWidget):
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
