from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import bidict, datatypes, get_repr, listdelegators


PanelModalityStr = Literal["none", "panel", "scene"]

PANEL_MODALITY: bidict[PanelModalityStr, QtWidgets.QGraphicsItem.PanelModality] = bidict(
    none=QtWidgets.QGraphicsItem.PanelModality.NonModal,
    panel=QtWidgets.QGraphicsItem.PanelModality.PanelModal,
    scene=QtWidgets.QGraphicsItem.PanelModality.SceneModal,
)

CacheModeStr = Literal["none", "item_coordinate", "device_coordinate"]

CACHE_MODE: bidict[CacheModeStr, QtWidgets.QGraphicsItem.CacheMode] = bidict(
    none=QtWidgets.QGraphicsItem.CacheMode.NoCache,
    item_coordinate=QtWidgets.QGraphicsItem.CacheMode.ItemCoordinateCache,
    device_coordinate=QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache,
)


class GraphicsItemMixin:
    def __repr__(self):
        return get_repr(self)

    def __contains__(self, value: QtCore.QPointF) -> bool:
        return self.contains(value)

    def __getitem__(self, key: int):
        return self.data(key)

    def __setitem__(self, key: int, value):
        self.setData(key, value)

    def set_focus(
        self, reason: constants.FocusReasonStr | constants.FocusReason = "other"
    ):
        self.setFocus(constants.FOCUS_REASONS.get_enum_value(reason))

    def colliding_items(
        self,
        mode: constants.ItemSelectionModeStr
        | constants.ItemSelectionMode = "intersects_shape",
    ) -> listdelegators.BaseListDelegator[QtWidgets.QGraphicsItem]:
        items = self.collidingItems(constants.ITEM_SELECTION_MODE.get_enum_value(mode))
        return listdelegators.BaseListDelegator(items)

    def collides_with(
        self,
        item: gui.QPainterPath | QtWidgets.QGraphicsItem,
        mode: constants.ItemSelectionModeStr
        | constants.ItemSelectionMode = "intersects_shape",
    ) -> bool:
        if isinstance(item, gui.QPainterPath):
            return self.collidesWithPath(
                item, constants.ITEM_SELECTION_MODE.get_enum_value(mode)
            )
        else:
            return self.collidesWithItem(
                item, constants.ITEM_SELECTION_MODE.get_enum_value(mode)
            )

    def set_panel_modality(
        self, modality: PanelModalityStr | QtWidgets.QGraphicsItem.PanelModality
    ):
        """Set panel modality.

        Args:
            modality: panel modality
        """
        self.setPanelModality(PANEL_MODALITY.get_enum_value(modality))

    def get_panel_modality(self) -> PanelModalityStr:
        """Get the current modality modes as a string.

        Returns:
            panel modality
        """
        return PANEL_MODALITY.inverse[self.panelModality()]

    def set_cache_mode(self, mode: CacheModeStr | QtWidgets.QGraphicsItem.CacheMode):
        """Set cache mode.

        Args:
            mode: cache mode
        """
        self.setCacheMode(CACHE_MODE.get_enum_value(mode))

    def get_cache_mode(self) -> CacheModeStr:
        """Get the current mode modes as a string.

        Returns:
            cache mode
        """
        return CACHE_MODE.inverse[self.cacheMode()]

    def get_shape(self) -> gui.PainterPath:
        return gui.PainterPath(self.shape())

    def set_scale(self, scale: tuple[float, float] | float):
        if isinstance(scale, float):
            self.setScale(scale)
        else:
            self.setTransform(gui.Transform.fromScale(scale[0], scale[1]), True)

    def set_transform(self, transform: datatypes.TransformType, combine: bool = False):
        if isinstance(transform, tuple):
            transform = gui.Transform(*transform)
        self.setTransform(transform, combine)


class GraphicsItem(GraphicsItemMixin, QtWidgets.QGraphicsItem):
    pass


if __name__ == "__main__":
    item = GraphicsItem()
