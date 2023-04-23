from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


SHAPE_MODE = bidict(
    mask=QtWidgets.QGraphicsPixmapItem.ShapeMode.MaskShape,
    bounding_rect=QtWidgets.QGraphicsPixmapItem.ShapeMode.BoundingRectShape,
    heuristic_mask=QtWidgets.QGraphicsPixmapItem.ShapeMode.HeuristicMaskShape,
)

ShapeModeStr = Literal["mask", "bounding_rect", "heuristic_mask"]


class GraphicsPixmapItem(widgets.GraphicsItemMixin, QtWidgets.QGraphicsPixmapItem):
    def set_transformation_mode(self, mode: constants.TransformationModeStr):
        """Set transformation mode.

        Args:
            mode: transformation mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in constants.TRANSFORMATION_MODE:
            raise InvalidParamError(mode, constants.TRANSFORMATION_MODE)
        self.setTransformationMode(constants.TRANSFORMATION_MODE[mode])

    def get_transformation_mode(self) -> constants.TransformationModeStr:
        """Return current transformation mode.

        Returns:
            transformation mode
        """
        return constants.TRANSFORMATION_MODE.inverse[self.transformationMode()]

    def set_shape_mode(self, mode: ShapeModeStr):
        """Set shape mode.

        Args:
            mode: shape mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in SHAPE_MODE:
            raise InvalidParamError(mode, SHAPE_MODE)
        self.setShapeMode(SHAPE_MODE[mode])

    def get_shape_mode(self) -> ShapeModeStr:
        """Return current shape mode.

        Returns:
            shape mode
        """
        return SHAPE_MODE.inverse[self.shapeMode()]

    def get_pixmap(self) -> gui.Pixmap | None:
        pix = self.pixmap()
        return None if pix.isNull() else gui.Pixmap(pix)
