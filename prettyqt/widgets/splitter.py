# -*- coding: utf-8 -*-

from typing import Union, Optional, List

from qtpy import QtCore, QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict, InvalidParamError


ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)


QtWidgets.QSplitter.__bases__ = (widgets.Frame,)


class Splitter(QtWidgets.QSplitter):
    def __init__(
        self,
        orientation: Union[str, int] = "horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if orientation in ORIENTATIONS:
            orientation = ORIENTATIONS[orientation]
        super().__init__(orientation, parent)

    def __getitem__(self, index: Union[int, str]):
        if isinstance(index, int):
            return self.widget(index)
        else:
            return self.findChild(QtWidgets.QWidget, index)

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
        self.__init__(state["orientation"])
        for item in state["items"]:
            self.addWidget(item)
        self.setHandleWidth(state["handle_width"])
        self.setChildrenCollapsible(state["children_collapsible"])
        self.setOpaqueResize(state["opaque_resize"])

    def __iter__(self):
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

    def add_layout(self, layout: QtWidgets.QLayout):
        widget = widgets.Widget()
        widget.set_layout(layout)
        self.addWidget(widget)

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
        orientation = "horizontal" if horizontal else "vertical"
        splitter = cls(orientation, parent=parent)
        for widget in widgets:
            splitter += widget
        return splitter

    def set_orientation(self, orientation: str):
        """Set the orientation of the splitter.

        Allowed values are "horizontal", "vertical"

        Args:
            orientation: orientation for the splitter

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in ORIENTATIONS:
            raise InvalidParamError(orientation, ORIENTATIONS)
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self) -> str:
        """Return current orientation.

        Possible values: "horizontal", "vertical"

        Returns:
            orientation
        """
        return ORIENTATIONS.inv[self.orientation()]


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Splitter()
    widget.show()
    app.main_loop()
