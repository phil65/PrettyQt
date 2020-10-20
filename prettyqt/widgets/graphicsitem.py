# -*- coding: utf-8 -*-

from typing import List, Union

from qtpy import QtWidgets, QtCore, QtGui

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError

ITEM_SELECTION_MODES = bidict(
    contains_shape=QtCore.Qt.ContainsItemShape,
    intersects_shape=QtCore.Qt.IntersectsItemShape,
    contains_bounding_rect=QtCore.Qt.ContainsItemBoundingRect,
    intersects_bounding_rect=QtCore.Qt.IntersectsItemBoundingRect,
)

FOCUS_REASONS = bidict(
    mouse=QtCore.Qt.MouseFocusReason,
    tab=QtCore.Qt.TabFocusReason,
    backtab=QtCore.Qt.BacktabFocusReason,
    active_window=QtCore.Qt.ActiveWindowFocusReason,
    popup=QtCore.Qt.PopupFocusReason,
    shortcut=QtCore.Qt.ShortcutFocusReason,
    menu_bar=QtCore.Qt.MenuBarFocusReason,
    other=QtCore.Qt.OtherFocusReason,
)

MODALITIES = bidict(
    none=QtWidgets.QGraphicsItem.NonModal,
    panel=QtWidgets.QGraphicsItem.PanelModal,
    scene=QtWidgets.QGraphicsItem.SceneModal,
)


class GraphicsItem(QtWidgets.QGraphicsItem):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __contains__(self, value: QtCore.QPointF) -> bool:
        return self.contains(value)

    def __getitem__(self, key: int):
        return self.data(key)

    def __setitem__(self, key: int, value):
        self.setData(key, value)

    def set_focus(self, reason: str = "other"):
        if reason not in FOCUS_REASONS:
            raise InvalidParamError(reason, FOCUS_REASONS)
        self.setFocus(FOCUS_REASONS[reason])

    def colliding_items(
        self, mode: str = "intersects_shape"
    ) -> List[QtWidgets.QGraphicsItem]:
        if mode not in ITEM_SELECTION_MODES:
            raise InvalidParamError(mode, ITEM_SELECTION_MODES)
        return self.collidingItems(ITEM_SELECTION_MODES[mode])

    def collides_with(
        self,
        item: Union[QtGui.QPainterPath, QtWidgets.QGraphicsItem],
        mode: str = "intersects_shape",
    ) -> bool:
        if mode not in ITEM_SELECTION_MODES:
            raise InvalidParamError(mode, ITEM_SELECTION_MODES)
        if isinstance(item, QtGui.QPainterPath):
            return self.collidesWithPath(item, ITEM_SELECTION_MODES[mode])
        else:
            return self.collidesWithItem(item, ITEM_SELECTION_MODES[mode])

    def set_panel_modality(self, modality: str = "window") -> None:
        """Set panel modality.

        Valid values for modality: "none", "panel", "scene"

        Args:
            modality: panel modality

        Raises:
            InvalidParamError: panel modality does not exist
        """
        if modality not in MODALITIES:
            raise InvalidParamError(modality, MODALITIES)
        self.setPanelModality(MODALITIES[modality])

    def get_panel_modality(self) -> str:
        """Get the current modality modes as a string.

        Possible values: "none", "panel", "scene"

        Returns:
            panel modality
            str
        """
        return MODALITIES.inv[self.panelModality()]

    def get_shape(self) -> gui.PainterPath:
        return gui.PainterPath(self.shape())
