from dataclasses import dataclass
from typing import List, Optional

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets


@dataclass
class ItemWrapper:
    item: QtWidgets.QWidgetItem
    position: int


class BorderLayout(widgets.Layout):
    West, North, South, East, Center = range(5)
    MinimumSize, SizeHint = range(2)

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        margin: int = 0,
        spacing: Optional[int] = None,
    ):
        super().__init__(parent)  # type: ignore
        self.set_margin(margin)
        self.setSpacing(spacing if spacing is not None else -1)
        self.items: List[ItemWrapper] = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QtWidgets.QWidgetItem):
        self.add_widgetitem(item, BorderLayout.West)

    def addWidget(self, widget: QtWidgets.QWidget, position: int = 0):
        self.add_widgetitem(widgets.WidgetItem(widget), position)

    def expandingDirections(self):
        return constants.HORIZONTAL | constants.VERTICAL

    def hasHeightForWidth(self) -> bool:
        return False

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int) -> Optional[QtWidgets.QWidgetItem]:  # type: ignore
        if index < len(self.items):
            return self.items[index].item
        return None

    def minimumSize(self):
        return self.calculate_size(BorderLayout.MinimumSize)

    def setGeometry(self, rect: QtCore.QRect):
        center = None
        east_width = 0
        west_width = 0
        north_height = 0
        south_height = 0

        super().setGeometry(rect)

        for wrapper in self.items:
            item = wrapper.item
            position = wrapper.position

            if position == BorderLayout.North:
                geom = core.Rect(
                    rect.x(), north_height, rect.width(), item.sizeHint().height()
                )
                item.setGeometry(geom)

                north_height += item.geometry().height() + self.spacing()

            elif position == BorderLayout.South:
                geom = core.Rect(
                    item.geometry().x(),
                    item.geometry().y(),
                    rect.width(),
                    item.sizeHint().height(),
                )
                item.setGeometry(geom)

                south_height += item.geometry().height() + self.spacing()
                geom = core.Rect(
                    rect.x(),
                    rect.y() + rect.height() - south_height + self.spacing(),
                    item.geometry().width(),
                    item.geometry().height(),
                )
                item.setGeometry(geom)

            elif position == BorderLayout.Center:
                center = wrapper

        center_height = rect.height() - north_height - south_height

        for wrapper in self.items:
            item = wrapper.item
            position = wrapper.position

            if position == BorderLayout.West:
                geom = core.Rect(
                    rect.x() + west_width,
                    north_height,
                    item.sizeHint().width(),
                    center_height,
                )
                item.setGeometry(geom)

                west_width += item.geometry().width() + self.spacing()

            elif position == BorderLayout.East:
                geom = core.Rect(
                    item.geometry().x(),
                    item.geometry().y(),
                    item.sizeHint().width(),
                    center_height,
                )
                item.setGeometry(geom)

                east_width += item.geometry().width() + self.spacing()

                geom = core.Rect(
                    rect.x() + rect.width() - east_width + self.spacing(),
                    north_height,
                    item.geometry().width(),
                    item.geometry().height(),
                )
                item.setGeometry(geom)

        if center:
            rect = core.Rect(
                west_width,
                north_height,
                rect.width() - east_width - west_width,
                center_height,
            )
            center.item.setGeometry(rect)

    def sizeHint(self) -> core.Size:
        return self.calculate_size(BorderLayout.SizeHint)

    def takeAt(self, index: int) -> Optional[QtWidgets.QWidgetItem]:  # type: ignore
        if 0 <= index < len(self.items):
            layout_struct = self.items.pop(index)
            return layout_struct.item

        return None

    def add_widgetitem(self, item: QtWidgets.QWidgetItem, position: int):
        self.items.append(ItemWrapper(item, position))

    def calculate_size(self, size_type: int) -> core.Size:
        total_size = core.Size()

        for wrapper in self.items:
            position = wrapper.position
            if size_type == BorderLayout.MinimumSize:
                item_size = wrapper.item.minimumSize()
            else:  # size_type == BorderLayout.SizeHint
                item_size = wrapper.item.sizeHint()

            if position in (BorderLayout.North, BorderLayout.South, BorderLayout.Center):
                total_size.setHeight(total_size.height() + item_size.height())

            if position in (BorderLayout.West, BorderLayout.East, BorderLayout.Center):
                total_size.setWidth(total_size.width() + item_size.width())

        return total_size


class Window(widgets.Widget):
    def __init__(self):
        super().__init__()

        central_widget = widgets.TextBrowser()
        central_widget.setPlainText("Central widget")

        layout = BorderLayout()
        layout.addWidget(central_widget, BorderLayout.Center)

        # Because BorderLayout doesn't call its super-class addWidget() it
        # doesn't take ownership of the widgets until setLayout() is called.
        # Therefore we keep a local reference to each label to prevent it being
        # garbage collected too soon.
        label_n = self.create_label("North")
        layout.addWidget(label_n, BorderLayout.North)

        label_w = self.create_label("West")
        layout.addWidget(label_w, BorderLayout.West)

        label_e1 = self.create_label("East 1")
        layout.addWidget(label_e1, BorderLayout.East)

        label_e2 = self.create_label("East 2")
        layout.addWidget(label_e2, BorderLayout.East)

        label_s = self.create_label("South")
        layout.addWidget(label_s, BorderLayout.South)

        self.setLayout(layout)

        self.setWindowTitle("Border Layout")

    @staticmethod
    def create_label(text: str):
        label = widgets.Label(text)
        label.setFrameStyle(widgets.Frame.Box | widgets.Frame.Raised)
        return label


if __name__ == "__main__":

    import sys

    app = widgets.app()
    window = Window()
    window.show()
    sys.exit(app.exec_())
