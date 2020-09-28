from typing import List

from qtpy import QtWidgets, QtCore

from prettyqt import core, widgets, gui, constants
from prettyqt.utils import InvalidParamError, bidict, helpers


ALIGNMENTS = bidict(
    left=constants.ALIGN_LEFT,
    right=constants.ALIGN_RIGHT,
    top=constants.ALIGN_TOP,
    bottom=constants.ALIGN_BOTTOM,
    top_left=constants.ALIGN_TOP_LEFT,
    top_right=constants.ALIGN_TOP_RIGHT,
    bottom_left=constants.ALIGN_BOTTOM_LEFT,
    bottom_right=constants.ALIGN_BOTTOM_RIGHT,
    center=constants.ALIGN_CENTER,
)

DRAG_MODES = bidict(
    none=QtWidgets.QGraphicsView.NoDrag,
    scroll_hand=QtWidgets.QGraphicsView.ScrollHandDrag,
    rubber_band=QtWidgets.QGraphicsView.RubberBandDrag,
)

CACHE_MODES = bidict(
    none=QtWidgets.QGraphicsView.CacheNone,
    background=QtWidgets.QGraphicsView.CacheBackground,
)

OPTIMIZATION_FLAGS = bidict(
    dont_clip_painter=QtWidgets.QGraphicsView.DontClipPainter,
    dont_save_painter_state=QtWidgets.QGraphicsView.DontSavePainterState,
    dont_adjust_for_antialiasing=QtWidgets.QGraphicsView.DontAdjustForAntialiasing,
)

VIEWPORT_ANCHORS = bidict(
    none=QtWidgets.QGraphicsView.NoAnchor,
    view_center=QtWidgets.QGraphicsView.AnchorViewCenter,
    under_mouse=QtWidgets.QGraphicsView.AnchorUnderMouse,
)

VIEWPORT_UPDATE_MODES = bidict(
    full=QtWidgets.QGraphicsView.FullViewportUpdate,
    minimal=QtWidgets.QGraphicsView.MinimalViewportUpdate,
    smart=QtWidgets.QGraphicsView.SmartViewportUpdate,
    bounding_rect=QtWidgets.QGraphicsView.BoundingRectViewportUpdate,
    none=QtWidgets.QGraphicsView.NoViewportUpdate,
)

ITEM_SELECTION_MODES = bidict(
    contains_shape=QtCore.Qt.ContainsItemShape,
    intersects_shape=QtCore.Qt.IntersectsItemShape,
    contains_bounding_rect=QtCore.Qt.ContainsItemBoundingRect,
    intersects_bounding_rect=QtCore.Qt.IntersectsItemBoundingRect,
)

SCENE_LAYERS = widgets.graphicsscene.SCENE_LAYERS  # type: ignore

RENDER_HINTS = gui.painter.RENDER_HINTS  # type: ignore

QtWidgets.QGraphicsView.__bases__ = (widgets.AbstractScrollArea,)


class GraphicsView(QtWidgets.QGraphicsView):
    def serialize_fields(self):
        return dict(
            scene=self.scene(),
            background_brush=gui.Brush(self.backgroundBrush()),
            foreground_brush=gui.Brush(self.foregroundBrush()),
            transformation_anchor=self.get_transformation_anchor(),
            resize_anchor=self.get_resize_anchor(),
            viewport_update_mode=self.get_viewport_update_mode(),
            drag_mode=self.get_drag_mode(),
            rubberband_selection_mode=self.get_rubberband_selection_mode(),
            scene_rect=core.RectF(self.sceneRect()),
            cache_mode=self.get_cache_mode(),
            is_interactive=self.isInteractive(),
        )

    def __getitem__(self, index: int):
        return self.items()[index]

    def invalidate_scene(self, rect: QtCore.QRectF, layer: str = "all"):
        if layer not in SCENE_LAYERS:
            raise InvalidParamError(layer, SCENE_LAYERS)
        self.invalidateScene(rect, SCENE_LAYERS[layer])

    def set_transformation_anchor(self, mode: str):
        """Set how the view should position the scene during transformations.

        Allowed values are "none", "view_center", "under_mouse"

        Args:
            mode: transformation anchor to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_ANCHORS:
            raise InvalidParamError(mode, VIEWPORT_ANCHORS)
        self.setTransformationAnchor(VIEWPORT_ANCHORS[mode])

    def get_transformation_anchor(self) -> str:
        """Return current transformation anchor.

        Possible values: "none", "view_center", "under_mouse"

        Returns:
            viewport anchor
        """
        return VIEWPORT_ANCHORS.inv[self.transformationAnchor()]

    def set_resize_anchor(self, mode: str):
        """Set how the view should position the scene during resizes.

        Allowed values are "none", "view_center", "under_mouse"

        Args:
            mode: resize anchor to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_ANCHORS:
            raise InvalidParamError(mode, VIEWPORT_ANCHORS)
        self.setResizeAnchor(VIEWPORT_ANCHORS[mode])

    def get_resize_anchor(self) -> str:
        """Return current resize anchor.

        Possible values: "none", "view_center", "under_mouse"

        Returns:
            resize anchor
        """
        return VIEWPORT_ANCHORS.inv[self.resizeAnchor()]

    def set_viewport_update_mode(self, mode: str):
        """Set how the viewport should update its contents.

        Allowed values are "full", "minimal", "smart", "bounding_rect", "none"

        Args:
            mode: viewport update mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_UPDATE_MODES:
            raise InvalidParamError(mode, VIEWPORT_UPDATE_MODES)
        self.setViewportUpdateMode(VIEWPORT_UPDATE_MODES[mode])

    def get_viewport_update_mode(self) -> str:
        """Return current viewport update mode.

        Possible values: "full", "minimal", "smart", "bounding_rect", "none"

        Returns:
            viewport update mode
        """
        return VIEWPORT_UPDATE_MODES.inv[self.viewportUpdateMode()]

    def set_drag_mode(self, mode: str):
        """Set the behavior for dragging the mouse while the left mouse button is pressed.

        Allowed values are "none", "scroll_hand", "rubber_band"

        Args:
            mode: drag mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in DRAG_MODES:
            raise InvalidParamError(mode, DRAG_MODES)
        self.setDragMode(DRAG_MODES[mode])

    def get_drag_mode(self) -> str:
        """Return current drag mode.

        Possible values: "none", "scroll_hand", "rubber_band"

        Returns:
            drag mode
        """
        return DRAG_MODES.inv[self.dragMode()]

    def set_rubberband_selection_mode(self, mode: str):
        """Set the behavior for selecting items with a rubber band selection rectangle.

        Allowed values are "contains_shape", "intersects_shape", "contains_bounding_rect",
        "intersects_bounding_rect"

        Args:
            mode: rubberband selection mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in ITEM_SELECTION_MODES:
            raise InvalidParamError(mode, ITEM_SELECTION_MODES)
        self.setRubberBandSelectionMode(ITEM_SELECTION_MODES[mode])

    def get_rubberband_selection_mode(self) -> str:
        """Return current rubberband selection mode.

        Possible values: "contains_shape", "intersects_shape", "contains_bounding_rect",
        "intersects_bounding_rect"

        Returns:
            rubberband selection mode
        """
        return ITEM_SELECTION_MODES.inv[self.rubberBandSelectionMode()]

    def set_cache_mode(self, mode: str):
        """Set the cache mode.

        Allowed values are "none", "background"

        Args:
            mode: cache mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in CACHE_MODES:
            raise InvalidParamError(mode, CACHE_MODES)
        self.setCacheMode(CACHE_MODES[mode])

    def get_cache_mode(self) -> str:
        """Return current cache mode.

        Possible values: "none", "background"

        Returns:
            cache mode
        """
        return CACHE_MODES.inv[self.cacheMode()]

    def set_optimization_flags(self, *items: str):
        for item in items:
            if item not in OPTIMIZATION_FLAGS:
                raise InvalidParamError(item, OPTIMIZATION_FLAGS)
        flags = helpers.merge_flags(items, OPTIMIZATION_FLAGS)
        self.setOptimizationFlags(flags)

    def get_optimization_flags(self) -> List[str]:
        return [k for k, v in OPTIMIZATION_FLAGS.items() if v & self.optimizationFlags()]


if __name__ == "__main__":
    app = widgets.app()
    view = GraphicsView()
    scene = widgets.GraphicsScene()
    scene.add_line(core.Line(0, 0, 200, 100))
    view.setScene(scene)
    view.show()
    app.main_loop()
