from __future__ import annotations

from collections.abc import Iterator

from typing_extensions import Self

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import listdelegators, InvalidParamError


class SplitterMixin(widgets.FrameMixin):
    def __init__(
        self,
        orientation: constants.OrientationStr | QtCore.Qt.Orientation = "horizontal",
        **kwargs,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, **kwargs)
        self.setHandleWidth(10)

    def __getitem__(self, index: int | str | slice) -> QtWidgets.QWidget:
        match index:
            case int():
                return self.widget(index)
            case str():
                result = self.find_child(QtWidgets.QWidget, index)
                if result is None:
                    raise KeyError("Widget not found")
                return result
            case slice():
                stop = index.stop or self.count()
                rng = range(index.start or 0, stop, index.step or 1)
                widgets = [self.widget(i) for i in rng]
                return listdelegators.SplitterDelegator(widgets, parent=self)
            case _:
                raise TypeError(index)

    def __setitem__(self, index: int, value: QtWidgets.QWidget):
        self.replaceWidget(index, value)

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.get_children())

    def __len__(self) -> int:
        return self.count()

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout):
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

    def get_children(self) -> list[QtWidgets.QWidget]:
        return [self.widget(i) for i in range(self.count())]

    def add_widget(
        self,
        widget: QtWidgets.QWidget,
        stretch: int | None = None,
        collapsible: bool = True,
        position: int | None = None,
    ) -> QtWidgets.QWidget:
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
        layout: QtWidgets.QLayout,
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
        item: QtWidgets.QWidget
        | QtWidgets.QLayout
        | list[QtWidgets.QWidget | QtWidgets.QLayout],
        stretch: int | None = None,
    ):
        match item:
            case QtWidgets.QWidget():
                self.add_widget(item, stretch=stretch)
            case QtWidgets.QLayout():
                self.add_layout(item)
            case list():
                for i in item:
                    self.add(i)
        return item

    @classmethod
    def from_widgets(
        cls,
        *widgets: QtWidgets.QWidget,
        horizontal: bool = False,
        parent: QtWidgets.QWidget | None = None,
    ) -> Self:
        splitter = cls("horizontal" if horizontal else "vertical", parent=parent)
        for widget in widgets:
            splitter += widget
        return splitter

    def set_orientation(self, orientation: constants.OrientationStr):
        """Set the orientation of the splitter.

        Args:
            orientation: orientation for the splitter

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in constants.ORIENTATION:
            raise InvalidParamError(orientation, constants.ORIENTATION)
        self.setOrientation(constants.ORIENTATION[orientation])

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]


class Splitter(SplitterMixin, QtWidgets.QSplitter):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = Splitter()
    widget.show()
    app.main_loop()
