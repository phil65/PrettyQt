from __future__ import annotations

from typing import TYPE_CHECKING, Self, overload

from prettyqt import constants, widgets
from prettyqt.utils import listdelegators


if TYPE_CHECKING:
    from collections.abc import Iterator


class SplitterMixin(widgets.FrameMixin):
    def __init__(
        self,
        orientation: constants.OrientationStr | constants.Orientation = "horizontal",
        **kwargs,
    ):
        super().__init__(constants.ORIENTATION.get_enum_value(orientation), **kwargs)
        self.setHandleWidth(10)

    @overload
    def __getitem__(self, index: int | str) -> widgets.QWidget: ...

    @overload
    def __getitem__(
        self, index: slice
    ) -> listdelegators.SplitterDelegator[widgets.QWidget]: ...

    def __getitem__(
        self, index: int | str | slice
    ) -> widgets.QWidget | listdelegators.SplitterDelegator[widgets.QWidget]:
        match index:
            case int():
                if index >= self.count():
                    raise IndexError(index)
                return self.widget(index)
            case str():
                result = self.find_child(widgets.QWidget, index)
                if result is None:
                    msg = "Widget not found"
                    raise KeyError(msg)
                return result
            case slice():
                stop = index.stop or self.count()
                rng = range(index.start or 0, stop, index.step or 1)
                wdgs = [self.widget(i) for i in rng]
                return listdelegators.SplitterDelegator(wdgs, parent=self)
            case _:
                raise TypeError(index)

    def __setitem__(self, index: int, value: widgets.QWidget):
        self.replaceWidget(index, value)

    def __iter__(self) -> Iterator[widgets.QWidget]:
        return iter(self.get_widgets())

    def __len__(self) -> int:
        return self.count()

    def __contains__(self, item: widgets.QWidget):
        return self.indexOf(item) >= 0

    def __add__(self, other: widgets.QWidget | widgets.QLayout):
        self.add(other)
        return self

    def __iadd__(self, item):
        self.add(item)
        return self

    def createHandle(self) -> widgets.SplitterHandle:
        return widgets.SplitterHandle(self.orientation(), self)

    # def saveState(self):
    #     sizes = self.sizes()
    #     if all(x == 0 for x in sizes):
    #         sizes = [10] * len(sizes)
    #     return {'sizes': sizes}

    # def restoreState(self, state):
    #     sizes = state['sizes']
    #     self.setSizes(sizes)
    #     for i in range(len(sizes)):
    #         self.setStretchFactor(i, sizes[i])

    def get_widgets(self) -> listdelegators.SplitterDelegator[widgets.QWidget]:
        widgets = [self.widget(i) for i in range(self.count())]
        return listdelegators.SplitterDelegator(widgets, parent=self)

    def add_widget(
        self,
        widget: widgets.QWidget,
        stretch: int | None = None,
        collapsible: bool = True,
        position: int | None = None,
    ) -> widgets.QWidget:
        if position is None:
            self.addWidget(widget)
        else:
            self.insertWidget(position, widget)
        index = self.indexOf(widget)
        if stretch is not None:
            self.setStretchFactor(index, stretch)
        self.setCollapsible(index, collapsible)
        return widget

    def add_layout(
        self,
        layout: widgets.QLayout,
        stretch: int | None = None,
        collapsible: bool = True,
        position: int | None = None,
    ) -> widgets.Widget:
        widget = widgets.Widget()
        widget.set_layout(layout)
        return self.add_widget(
            widget, stretch=stretch, collapsible=collapsible, position=position
        )

    def add(
        self,
        item: widgets.QWidget | widgets.QLayout | list[widgets.QWidget | widgets.QLayout],
        stretch: int | None = None,
    ):
        match item:
            case widgets.QWidget():
                self.add_widget(item, stretch=stretch)
            case widgets.QLayout():
                self.add_layout(item)
            case list():
                for i in item:
                    self.add(i)
        return item

    @classmethod
    def from_widgets(
        cls,
        *widgets: widgets.QWidget,
        horizontal: bool = False,
        parent: widgets.QWidget | None = None,
    ) -> Self:
        splitter = cls("horizontal" if horizontal else "vertical", parent=parent)
        for widget in widgets:
            splitter += widget
        return splitter

    def set_orientation(
        self, orientation: constants.OrientationStr | constants.Orientation
    ):
        """Set the orientation of the splitter.

        Args:
            orientation: orientation for the splitter

        """
        self.setOrientation(constants.ORIENTATION.get_enum_value(orientation))

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]

    def set_sizes(self, sizes: list[int]):
        """Set the sizes of the splitter.

        Args:
            sizes: sizes for the splitter

        """
        self.setSizes(sizes)


class Splitter(SplitterMixin, widgets.QSplitter):
    """Implements a splitter widget."""


if __name__ == "__main__":
    app = widgets.app()
    widget = Splitter()
    widget.show()
    app.exec()
