from typing import List

from qtpy import QtWidgets, QtGui, QtCore

from prettyqt import core, widgets
from prettyqt.utils import InvalidParamError, bidict


ITEM_SELECTION_MODES = bidict(
    contains_shape=QtCore.Qt.ContainsItemShape,
    intersects_shape=QtCore.Qt.IntersectsItemShape,
    contains_bounding_rect=QtCore.Qt.ContainsItemBoundingRect,
    intersects_bounding_rect=QtCore.Qt.IntersectsItemBoundingRect,
)

QtWidgets.QGraphicsScene.__bases__ = (core.Object,)


class GraphicsScene(QtWidgets.QGraphicsScene):
    def __getitem__(self, index: int):
        return self.items()[index]

    def add(self, item) -> QtWidgets.QGraphicsItem:
        if isinstance(item, QtWidgets.QGraphicsItem):
            self.addItem(item)
            return item
        elif isinstance(item, QtGui.QPixmap):
            g_item = widgets.GraphicsPixmapItem()
            g_item.setPixmap(item)
            self.addItem(g_item)
            return g_item

    def colliding_items(
        self, item: QtWidgets.QGraphicsItem, mode: str = "intersects_shape"
    ) -> List[QtWidgets.QGraphicsItem]:
        if mode not in ITEM_SELECTION_MODES:
            raise InvalidParamError(mode, ITEM_SELECTION_MODES)
        return self.collidingItems(item, ITEM_SELECTION_MODES[mode])
