from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


class GraphicsAnchorLayout(widgets.GraphicsLayoutMixin, QtWidgets.QGraphicsAnchorLayout):
    def add_anchor(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_edge: constants.AnchorPointStr,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_edge: constants.AnchorPointStr,
    ) -> QtWidgets.QGraphicsAnchor:
        return self.addAnchor(
            first_item,
            constants.ANCHOR_POINT[first_edge],
            second_item,
            constants.ANCHOR_POINT[second_edge],
        )

    def get_anchor(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_edge: constants.AnchorPointStr,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_edge: constants.AnchorPointStr,
    ) -> QtWidgets.QGraphicsAnchor:
        return self.anchor(
            first_item,
            constants.ANCHOR_POINT[first_edge],
            second_item,
            constants.ANCHOR_POINT[second_edge],
        )

    def add_anchors(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        second_item: QtWidgets.QGraphicsLayoutItem,
        orientation: constants.OrientationStr | constants.Orientation,
    ):
        self.addAnchors(
            first_item, second_item, constants.ORIENTATION.get_enum_value(orientation)
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
