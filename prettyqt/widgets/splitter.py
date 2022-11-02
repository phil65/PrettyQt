from __future__ import annotations

from collections.abc import Iterator

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QSplitter.__bases__ = (widgets.Frame,)


class Splitter(QtWidgets.QSplitter):
    def __init__(
        self,
        orientation: (constants.OrientationStr | QtCore.Qt.Orientation) = "horizontal",
        parent: QtWidgets.QWidget | None = None,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent)

    def __getitem__(self, index: int | str) -> QtWidgets.QWidget:
        if isinstance(index, int):
            return self.widget(index)
        else:
            result = self.find_child(QtWidgets.QWidget, index)
            if result is None:
                raise KeyError("Widget not found")
            return result

    def __setitem__(self, index: int, value: QtWidgets.QWidget):
        self.replaceWidget(index, value)

    def serialize_fields(self):
        return dict(
            items=self.get_children(),
            orientation=self.get_orientation(),
            handle_width=self.handleWidth(),
            children_collapsible=self.childrenCollapsible(),
            opaque_resize=self.opaqueResize(),
        )

    def __setstate__(self, state):
        for item in state["items"]:
            self.addWidget(item)
        self.setHandleWidth(state["handle_width"])
        self.setChildrenCollapsible(state["children_collapsible"])
        self.setOpaqueResize(state["opaque_resize"])

    def __reduce__(self):
        return type(self), (self.orientation(),), self.__getstate__()

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.get_children())

    def __len__(self) -> int:
        return self.count()

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout):
        self.add(other)
        return self

    def get_children(self) -> list[QtWidgets.QWidget]:
        return [self[i] for i in range(self.count())]

    def add_widget(self, widget: QtWidgets.QWidget):
        self.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout) -> widgets.Widget:
        widget = widgets.Widget()
        widget.set_layout(layout)
        self.addWidget(widget)
        return widget

    def add(self, *item: QtWidgets.QWidget | QtWidgets.QLayout):
        for i in item:
            if isinstance(i, QtWidgets.QWidget):
                self.add_widget(i)
            else:
                self.add_layout(i)

    @classmethod
    def from_widgets(
        cls,
        *widgets: QtWidgets.QWidget,
        horizontal: bool = False,
        parent: QtWidgets.QWidget | None = None,
    ):
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


if __name__ == "__main__":
    app = widgets.app()
    widget = Splitter()
    widget.show()
    app.main_loop()
