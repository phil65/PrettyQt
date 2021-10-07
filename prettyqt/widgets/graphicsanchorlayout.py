from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


EDGE = bidict(
    left=QtCore.Qt.AnchorPoint.AnchorLeft,
    horizontal_center=QtCore.Qt.AnchorPoint.AnchorHorizontalCenter,
    right=QtCore.Qt.AnchorPoint.AnchorRight,
    top=QtCore.Qt.AnchorPoint.AnchorTop,
    vertical_center=QtCore.Qt.AnchorPoint.AnchorVerticalCenter,
    bottom=QtCore.Qt.AnchorPoint.AnchorBottom,
)

EdgeStr = Literal[
    "left", "horizontal_center", "right", "top", "vertical_center", "bottom"
]

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
        orientation: constants.OrientationStr,
    ):
        if orientation not in constants.ORIENTATION:
            raise InvalidParamError(orientation, constants.ORIENTATION)
        self.addAnchors(
            first_item, second_item, constants.ORIENTATION[orientation]  # type: ignore
        )

    def add_corner_anchors(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_corner: constants.CornerStr,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_corner: constants.CornerStr,
    ):
        self.addCornerAnchors(
            first_item,
            constants.CORNER[first_corner],
            second_item,
            constants.CORNER[second_corner],
        )


if __name__ == "__main__":
    app = widgets.app()
    layout = GraphicsAnchorLayout()
