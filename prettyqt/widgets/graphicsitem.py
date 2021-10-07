from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


PANEL_MODALITY = bidict(
    none=QtWidgets.QGraphicsItem.PanelModality.NonModal,
    panel=QtWidgets.QGraphicsItem.PanelModality.PanelModal,
    scene=QtWidgets.QGraphicsItem.PanelModality.SceneModal,
)

PanelModalityStr = Literal["none", "panel", "scene"]

CACHE_MODE = bidict(
    none=QtWidgets.QGraphicsItem.CacheMode.NoCache,
    item_coordinate=QtWidgets.QGraphicsItem.CacheMode.ItemCoordinateCache,
    device_coordinate=QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache,
)

CacheModeStr = Literal["none", "item_coordinate", "device_coordinate"]


class GraphicsItem(QtWidgets.QGraphicsItem):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __contains__(self, value: QtCore.QPointF) -> bool:
        return self.contains(value)

    def __getitem__(self, key: int):
        return self.data(key)

    def __setitem__(self, key: int, value):
        self.setData(key, value)

    def serialize_fields(self):
        return dict(
            cache_mode=self.get_cache_mode(),
            accept_drops=self.acceptDrops(),
            accept_hover_events=self.acceptHoverEvents(),
            accept_touch_events=self.acceptTouchEvents(),
            bounding_region_granularity=self.boundingRegionGranularity(),
            enabled=self.isEnabled(),
            filters_child_events=self.filtersChildEvents(),
            opacity=self.opacity(),
            panel_modality=self.get_panel_modality(),
            pos=self.pos(),
            rotation=self.rotation(),
            scale=self.scale(),
            selected=self.isSelected(),
            tool_tip=self.toolTip(),
            transform_origin_point=self.transformOriginPoint(),
            visible=self.isVisible(),
            z_value=self.zValue(),
        )

    def set_focus(self, reason: constants.FocusReasonStr = "other"):
        if reason not in constants.FOCUS_REASONS:
            raise InvalidParamError(reason, constants.FOCUS_REASONS)
        self.setFocus(constants.FOCUS_REASONS[reason])

    def colliding_items(
        self, mode: constants.ItemSelectionModeStr = "intersects_shape"
    ) -> list[QtWidgets.QGraphicsItem]:
        if mode not in constants.ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, constants.ITEM_SELECTION_MODE)
        return self.collidingItems(constants.ITEM_SELECTION_MODE[mode])

    def collides_with(
        self,
        item: QtGui.QPainterPath | QtWidgets.QGraphicsItem,
        mode: constants.ItemSelectionModeStr = "intersects_shape",
    ) -> bool:
        if mode not in constants.ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, constants.ITEM_SELECTION_MODE)
        if isinstance(item, QtGui.QPainterPath):
            return self.collidesWithPath(item, constants.ITEM_SELECTION_MODE[mode])
        else:
            return self.collidesWithItem(item, constants.ITEM_SELECTION_MODE[mode])

    def set_panel_modality(self, modality: PanelModalityStr) -> None:
        """Set panel modality.

        Args:
            modality: panel modality

        Raises:
            InvalidParamError: panel modality does not exist
        """
        if modality not in PANEL_MODALITY:
            raise InvalidParamError(modality, PANEL_MODALITY)
        self.setPanelModality(PANEL_MODALITY[modality])

    def get_panel_modality(self) -> PanelModalityStr:
        """Get the current modality modes as a string.

        Returns:
            panel modality
        """
        return PANEL_MODALITY.inverse[self.panelModality()]

    def set_cache_mode(self, mode: CacheModeStr) -> None:
        """Set cache mode.

        Args:
            mode: cache mode

        Raises:
            InvalidParamError: cache mode does not exist
        """
        if mode not in CACHE_MODE:
            raise InvalidParamError(mode, CACHE_MODE)
        self.setCacheMode(CACHE_MODE[mode])

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


if __name__ == "__main__":
    item = GraphicsItem()
