from typing import List, Union, Literal

from qtpy import QtWidgets, QtCore, QtGui

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError

ITEM_SELECTION_MODE = bidict(
    contains_shape=QtCore.Qt.ContainsItemShape,
    intersects_shape=QtCore.Qt.IntersectsItemShape,
    contains_bounding_rect=QtCore.Qt.ContainsItemBoundingRect,
    intersects_bounding_rect=QtCore.Qt.IntersectsItemBoundingRect,
)

ItemSelectionModeStr = Literal[
    "contains_shape",
    "intersects_shape",
    "contains_bounding_rect",
    "intersects_bounding_rect",
]

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

MODALITY = bidict(
    none=QtWidgets.QGraphicsItem.NonModal,
    panel=QtWidgets.QGraphicsItem.PanelModal,
    scene=QtWidgets.QGraphicsItem.SceneModal,
)

PanelModalityStr = Literal["none", "panel", "scene"]


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
        self, mode: ItemSelectionModeStr = "intersects_shape"
    ) -> List[QtWidgets.QGraphicsItem]:
        if mode not in ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, ITEM_SELECTION_MODE)
        return self.collidingItems(ITEM_SELECTION_MODE[mode])

    def collides_with(
        self,
        item: Union[QtGui.QPainterPath, QtWidgets.QGraphicsItem],
        mode: ItemSelectionModeStr = "intersects_shape",
    ) -> bool:
        if mode not in ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, ITEM_SELECTION_MODE)
        if isinstance(item, QtGui.QPainterPath):
            return self.collidesWithPath(item, ITEM_SELECTION_MODE[mode])
        else:
            return self.collidesWithItem(item, ITEM_SELECTION_MODE[mode])

    def set_panel_modality(self, modality: PanelModalityStr) -> None:
        """Set panel modality.

        Args:
            modality: panel modality

        Raises:
            InvalidParamError: panel modality does not exist
        """
        if modality not in MODALITY:
            raise InvalidParamError(modality, MODALITY)
        self.setPanelModality(MODALITY[modality])

    def get_panel_modality(self) -> PanelModalityStr:
        """Get the current modality modes as a string.

        Returns:
            panel modality
        """
        return MODALITY.inverse[self.panelModality()]

    def get_shape(self) -> gui.PainterPath:
        return gui.PainterPath(self.shape())


if __name__ == "__main__":
    item = GraphicsItem()
