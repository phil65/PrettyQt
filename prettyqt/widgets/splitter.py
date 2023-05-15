from __future__ import annotations

from collections.abc import Iterator

from typing_extensions import Self

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError


class SplitterMixin(widgets.FrameMixin):
    def __init__(
        self,
        orientation: (constants.OrientationStr | QtCore.Qt.Orientation) = "horizontal",
        **kwargs,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __getitem__(self, index: int | str) -> QtWidgets.QWidget:
        if isinstance(index, int):
            return self.widget(index)
        result = self.find_child(QtWidgets.QWidget, index)
        if result is None:
            raise KeyError("Widget not found")
        return result

    def __setitem__(self, index: int, value: QtWidgets.QWidget):
        self.replaceWidget(index, value)

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

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.get_children())

    def __len__(self) -> int:
        return self.count()

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout):
        self.add(other)
        return self

    def createHandle(self) -> widgets.SplitterHandle:
        return widgets.SplitterHandle(self.orientation(), self)

    def get_children(self) -> list[QtWidgets.QWidget]:
        return [self[i] for i in range(self.count())]

    def add_widget(
        self,
        widget: QtWidgets.QWidget,
        stretch: int | None = None,
        collapsible: bool = True,
        position: int | None = None,
    ):
        if position is None:
            self.addWidget(widget)
        else:
            self.insertWidget(position, widget)
        index = self.indexOf(widget)
        if stretch is not None:
            self.setStretchFactor(index, stretch)
        self.setCollapsible(index, collapsible)

    def add_layout(self, layout: QtWidgets.QLayout) -> widgets.Widget:
        widget = widgets.Widget()
        widget.set_layout(layout)
        self.addWidget(widget)
        return widget

    def add(
        self, *item: QtWidgets.QWidget | QtWidgets.QLayout, stretch: int | None = None
    ):
        for i in item:
            if isinstance(i, QtWidgets.QWidget):
                self.add_widget(i)
            else:
                self.add_layout(i)
            if stretch is not None:
                self.setStretchFactor(self.count() - 1, stretch)

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
