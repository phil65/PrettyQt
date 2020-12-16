from typing import List, Literal, Union

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import constants, gui
from prettyqt.utils import InvalidParamError, bidict


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

    def set_focus(self, reason: constants.FocusReasonStr = "other"):
        if reason not in constants.FOCUS_REASONS:
            raise InvalidParamError(reason, constants.FOCUS_REASONS)
        self.setFocus(constants.FOCUS_REASONS[reason])

    def colliding_items(
        self, mode: constants.ItemSelectionModeStr = "intersects_shape"
    ) -> List[QtWidgets.QGraphicsItem]:
        if mode not in constants.ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, constants.ITEM_SELECTION_MODE)
        return self.collidingItems(constants.ITEM_SELECTION_MODE[mode])

    def collides_with(
        self,
        item: Union[QtGui.QPainterPath, QtWidgets.QGraphicsItem],
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
