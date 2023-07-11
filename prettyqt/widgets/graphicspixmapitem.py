from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.utils import bidict


ShapeModeStr = Literal["mask", "bounding_rect", "heuristic_mask"]

SHAPE_MODE: bidict[ShapeModeStr, widgets.QGraphicsPixmapItem.ShapeMode] = bidict(
    mask=widgets.QGraphicsPixmapItem.ShapeMode.MaskShape,
    bounding_rect=widgets.QGraphicsPixmapItem.ShapeMode.BoundingRectShape,
    heuristic_mask=widgets.QGraphicsPixmapItem.ShapeMode.HeuristicMaskShape,
)


class GraphicsPixmapItem(widgets.GraphicsItemMixin, widgets.QGraphicsPixmapItem):
    """Pixmap item that you can add to a QGraphicsScene."""

    def set_transformation_mode(
        self, mode: constants.TransformationModeStr | constants.TransformationMode
    ):
        """Set transformation mode.

        Args:
            mode: transformation mode to use
        """
        self.setTransformationMode(constants.TRANSFORMATION_MODE.get_enum_value(mode))

    def get_transformation_mode(self) -> constants.TransformationModeStr:
        """Return current transformation mode.

        Returns:
            transformation mode
        """
        return constants.TRANSFORMATION_MODE.inverse[self.transformationMode()]

    def set_shape_mode(self, mode: ShapeModeStr | widgets.QGraphicsPixmapItem.ShapeMode):
        """Set shape mode.

        Args:
            mode: shape mode to use
        """
        self.setShapeMode(SHAPE_MODE.get_enum_value(mode))

    def get_shape_mode(self) -> ShapeModeStr:
        """Return current shape mode.

        Returns:
            shape mode
        """
        return SHAPE_MODE.inverse[self.shapeMode()]

    def get_pixmap(self) -> gui.Pixmap | None:
        pix = self.pixmap()
        return None if pix.isNull() else gui.Pixmap(pix)
