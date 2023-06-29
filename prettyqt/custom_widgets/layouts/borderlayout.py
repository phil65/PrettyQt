from __future__ import annotations

from dataclasses import dataclass
import enum

from typing import Literal

from prettyqt import constants, core, widgets


@dataclass
class ItemWrapper:
    item: widgets.QWidgetItem
    position: BorderLayout.Position


class BorderLayout(widgets.Layout):
    ID = "border"

    class Position(enum.IntEnum):
        """Item position."""

        West = 0
        North = 1
        South = 2
        East = 3
        Center = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items: list[ItemWrapper] = []

    def addItem(self, item: widgets.QWidgetItem):
        self.add_widgetitem(item, BorderLayout.Position.West)

    def addWidget(
        self,
        widget: widgets.QWidget,
        position: Position | None = None,
    ):
        position = BorderLayout.Position.West if position is None else position
        self.add_widgetitem(widgets.WidgetItem(widget), position)

    def expandingDirections(self) -> constants.Orientation:
        return constants.HORIZONTAL | constants.VERTICAL

    def hasHeightForWidth(self) -> bool:
        return False

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int) -> widgets.QWidgetItem | None:
        return self.items[index].item if index < len(self.items) else None

    def minimumSize(self):
        return self.calculate_size("minimum")

    def setGeometry(self, rect: core.QRect):
        center = None
        east_width = 0
        west_width = 0
        north_height = 0
        south_height = 0
        super().setGeometry(rect)
        for wrapper in self.items:
            item = wrapper.item
            match wrapper.position:
                case BorderLayout.Position.North:
                    h = item.sizeHint().height()
                    geom = core.Rect(rect.x(), north_height, rect.width(), h)
                    item.setGeometry(geom)
                    north_height += item.geometry().height() + self.spacing()
                case BorderLayout.Position.South:
                    geo = item.geometry()
                    h = item.sizeHint().height()
                    geom = core.Rect(geo.x(), geo.y(), rect.width(), h)
                    item.setGeometry(geom)
                    south_height += item.geometry().height() + self.spacing()
                    y = rect.y() + rect.height() - south_height + self.spacing()
                    geo = item.geometry()
                    geom = core.Rect(rect.x(), y, geo.width(), geo.height())
                    item.setGeometry(geom)
                case BorderLayout.Position.Center:
                    center = wrapper

        center_height = rect.height() - north_height - south_height

        for wrapper in self.items:
            item = wrapper.item
            match wrapper.position:
                case BorderLayout.Position.West:
                    x = rect.x() + west_width
                    w = item.sizeHint().width()
                    geom = core.Rect(x, north_height, w, center_height)
                    item.setGeometry(geom)
                    west_width += item.geometry().width() + self.spacing()
                case BorderLayout.Position.East:
                    geo = item.geometry()
                    w = item.sizeHint().width()
                    geom = core.Rect(geo.x(), geo.y(), w, center_height)
                    item.setGeometry(geom)
                    east_width += item.geometry().width() + self.spacing()
                    x = rect.x() + rect.width() - east_width + self.spacing()
                    geom = core.Rect(x, north_height, geo.width(), geo.height())
                    item.setGeometry(geom)

        if center:
            w = rect.width() - east_width - west_width
            rect = core.Rect(west_width, north_height, w, center_height)
            center.item.setGeometry(rect)

    def sizeHint(self) -> core.Size:
        return self.calculate_size("size_hint")

    def takeAt(self, index: int) -> widgets.QWidgetItem | None:
        if 0 <= index < len(self.items):
            layout_struct = self.items.pop(index)
            return layout_struct.item

        return None

    def add_widgetitem(self, item: widgets.QWidgetItem, position: Position):
        self.items.append(ItemWrapper(item, position))

    def calculate_size(self, size_type: Literal["minimum", "size_hint"]) -> core.Size:
        total_size = core.Size()
        Pos = BorderLayout.Position
        for wrapper in self.items:
            item_size = (
                wrapper.item.minimumSize()
                if size_type == "minimum"
                else wrapper.item.sizeHint()
            )
            if wrapper.position in (Pos.North, Pos.South, Pos.Center):
                total_size.setHeight(total_size.height() + item_size.height())
            if wrapper.position in (Pos.West, Pos.East, Pos.Center):
                total_size.setWidth(total_size.width() + item_size.width())
        return total_size


if __name__ == "__main__":

    class Window(widgets.Widget):
        def __init__(self):
            super().__init__()

            central_widget = widgets.TextBrowser()
            central_widget.setPlainText("Central widget")

            layout = BorderLayout()
            layout.addWidget(central_widget, BorderLayout.Position.Center)

            # Because BorderLayout doesn't call its super-class addWidget() it
            # doesn't take ownership of the widgets until setLayout() is called.
            # Therefore we keep a local reference to each label to prevent it being
            # garbage collected too soon.
            label_n = self.create_label("North")
            layout.addWidget(label_n, BorderLayout.Position.North)
            label_w = self.create_label("West")
            layout.addWidget(label_w, BorderLayout.Position.West)
            label_e1 = self.create_label("East 1")
            layout.addWidget(label_e1, BorderLayout.Position.East)
            label_e2 = self.create_label("East 2")
            layout.addWidget(label_e2, BorderLayout.Position.East)
            label_s = self.create_label("South")
            layout.addWidget(label_s, BorderLayout.Position.South)
            self.setLayout(layout)
            self.setWindowTitle("Border Layout")

        @staticmethod
        def create_label(text: str):
            label = widgets.Label(text)
            label.setFrameStyle(widgets.Frame.Shape.Box | widgets.Frame.Shadow.Raised)
            return label

    app = widgets.app()
    window = Window()
    window.show()
    app.exec()
