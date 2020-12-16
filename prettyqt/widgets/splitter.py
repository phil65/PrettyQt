from typing import Iterator, List, Optional, Union

from qtpy import QtWidgets

from prettyqt import constants, widgets
from prettyqt.utils import InvalidParamError


QtWidgets.QSplitter.__bases__ = (widgets.Frame,)


class Splitter(QtWidgets.QSplitter):
    def __init__(
        self,
        orientation: Union[constants.OrientationStr, int] = "horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if orientation in constants.ORIENTATION:
            orientation = constants.ORIENTATION[orientation]
        super().__init__(orientation, parent)

    def __getitem__(self, index: Union[int, str]) -> QtWidgets.QWidget:
        if isinstance(index, int):
            return self.widget(index)
        else:
            result = self.findChild(QtWidgets.QWidget, index)
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

    def __add__(self, other: Union[QtWidgets.QWidget, QtWidgets.QLayout]):
        if isinstance(other, (QtWidgets.QLayout, QtWidgets.QWidget)):
            self.add(other)
            return self
        raise TypeError(f"Invalid type: {type(other)}")

    def get_children(self) -> List[QtWidgets.QWidget]:
        return [self[i] for i in range(self.count())]

    def add_widget(self, widget: QtWidgets.QWidget):
        self.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout) -> widgets.Widget:
        widget = widgets.Widget()
        widget.set_layout(layout)
        self.addWidget(widget)
        return widget

    def add(self, *item: Union[QtWidgets.QWidget, QtWidgets.QLayout]):
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
        parent: Optional[QtWidgets.QWidget] = None,
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
    app = QtWidgets.QApplication([])
    widget = Splitter()
    widget.show()
    app.main_loop()
