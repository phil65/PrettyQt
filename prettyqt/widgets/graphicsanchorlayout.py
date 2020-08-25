from qtpy import QtWidgets, QtCore

from prettyqt import widgets
from prettyqt.utils import bidict

ANCHORS = bidict(
    left=QtCore.Qt.AnchorLeft,
    horizontal_center=QtCore.Qt.AnchorHorizontalCenter,
    right=QtCore.Qt.AnchorRight,
    top=QtCore.Qt.AnchorTop,
    vertical_center=QtCore.Qt.AnchorVerticalCenter,
    bottom=QtCore.Qt.AnchorBottom,
)

CORNERS = bidict(
    top_left=QtCore.Qt.TopLeftCorner,
    top_right=QtCore.Qt.TopRightCorner,
    bottom_left=QtCore.Qt.BottomLeftCorner,
    bottom_right=QtCore.Qt.BottomRightCorner,
)

QtWidgets.QGraphicsAnchorLayout.__bases__ = (widgets.GraphicsLayout,)


class GraphicsAnchorLayout(QtWidgets.QGraphicsAnchorLayout):
    def add_anchor(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_edge: str,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_edge: str,
    ):
        self.addAnchor(first_item, ANCHORS[first_edge], second_item, ANCHORS[second_edge])

    def get_anchor(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_edge: str,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_edge: str,
    ):
        return self.anchor(
            first_item, ANCHORS[first_edge], second_item, ANCHORS[second_edge]
        )

    def add_anchors(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        second_item: QtWidgets.QGraphicsLayoutItem,
        orientation: str,
    ):
        if orientation == "horizontal":
            orientation = QtCore.Qt.Horizontal
        elif orientation == "vertical":
            orientation = QtCore.Qt.Vertical
        else:
            raise ValueError()
        self.addAnchors(first_item, second_item, orientation)

    def add_corner_anchors(
        self,
        first_item: QtWidgets.QGraphicsLayoutItem,
        first_corner: str,
        second_item: QtWidgets.QGraphicsLayoutItem,
        second_corner: str,
    ):
        self.addCornerAnchors(
            first_item, CORNERS[first_corner], second_item, CORNERS[second_corner]
        )


if __name__ == "__main__":
    app = widgets.app()
    layout = GraphicsAnchorLayout()
