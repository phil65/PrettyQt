from typing import Literal

from qtpy import QtWidgets, QtCore

from prettyqt import widgets
from prettyqt.utils import bidict

EDGE = bidict(
    left=QtCore.Qt.AnchorLeft,
    horizontal_center=QtCore.Qt.AnchorHorizontalCenter,
    right=QtCore.Qt.AnchorRight,
    top=QtCore.Qt.AnchorTop,
    vertical_center=QtCore.Qt.AnchorVerticalCenter,
    bottom=QtCore.Qt.AnchorBottom,
)

EdgeStr = Literal[
    "left", "horizontal_center", "right", "top", "vertical_center", "bottom"
]

CORNER = bidict(
    top_left=QtCore.Qt.TopLeftCorner,
    top_right=QtCore.Qt.TopRightCorner,
    bottom_left=QtCore.Qt.BottomLeftCorner,
    bottom_right=QtCore.Qt.BottomRightCorner,
)

CornerStr = Literal["top_left", "top_right", "bottom_left", "bottom_right"]

QtWidgets.QGraphicsAnchorLayout.__bases__ = (widgets.GraphicsLayout,)


class GraphicsAnchorLayout(QtWidgets.QGraphicsAnchorLayout):
    def add_anchor(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_edge: EdgeStr,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_edge: EdgeStr,
    ) -> QtWidgets.QGraphicsAnchor:
        return self.addAnchor(
            first_item, EDGE[first_edge], second_item, EDGE[second_edge]
        )

    def get_anchor(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_edge: EdgeStr,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_edge: EdgeStr,
    ) -> QtWidgets.QGraphicsAnchor:
        return self.anchor(first_item, EDGE[first_edge], second_item, EDGE[second_edge])

    def add_anchors(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        second_item: QtWidgets.QGraphicsLayoutItem,
        orientation: Literal["horizontal", "vertical"],
    ):
        if orientation == "horizontal":
            flag = QtCore.Qt.Horizontal
        elif orientation == "vertical":
            flag = QtCore.Qt.Vertical
        else:
            raise ValueError()
        self.addAnchors(first_item, second_item, flag)

    def add_corner_anchors(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_corner: CornerStr,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_corner: CornerStr,
    ):
        self.addCornerAnchors(
            first_item, CORNER[first_corner], second_item, CORNER[second_corner]
        )


if __name__ == "__main__":
    app = widgets.app()
    layout = GraphicsAnchorLayout()
